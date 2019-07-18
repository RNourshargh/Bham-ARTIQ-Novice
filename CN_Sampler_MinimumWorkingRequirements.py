from artiq.experiment import *
import numpy as np


class Test(EnvExperiment):
    """Sampler"""
    def build(self):
        self.setattr_device("core")
        self.setattr_device("sampler0")
        self.queue = []

    @rpc(flags={"async"})               
    def cb(self, data):
        self.queue.append(data)                         #adds "data" list to queue 

    def run(self):
        
        self.sample()                                   #runs sample function
        data = np.array(self.queue)                     #generates array in current context and populates it with queued values
        
        for i in range(1024):
            self.mutate_dataset("samples",i,data[0][i])
            #print(data[0][i])                           #prints data from channel 0 
            

    @kernel
    def sample(self):
        channels = 8                                    #runs on all 8 channels
        d = [[0]*channels for i in range(1024)]         #d is a  8x1024 int array used to store sampler data
        acqs = len(d)                                   #number of samples is given by the length of "d"
        self.core.reset()                               
        dev = self.sampler0                             #sets sampler0 a card to be used
        dev.init()                                      #initialises sampler
        
        for i in range(acqs):                           #loops over number of samples
            dev.sample_mu(d[i])                         #runs sampler, saves to d
            delay(6*us)                                 #6us delay minimum
        
        self.cb(d)                                      #move data to queue
        self.core.break_realtime()                  
