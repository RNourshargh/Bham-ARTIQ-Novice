from artiq.experiment import *
import numpy as np


class Test(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("sampler0")
        self.queue = []

    @rpc(flags={"async"})               
    def cb(self, data):
        self.queue.append(data)                         #adds whatever is passed into it into a queue

    def run(self):
        
        self.sample()                                   #runs sampler code
        data = np.array(self.queue)                     #generates array in current context and populates it with queued values
        
        for i in range(1024):
            print(data[0][i][0])                        #prints data from channel 0 in the 10th run

    @kernel
    def sample(self):
        channels = 8                                    #runs on 8 channels
        d = [[0]*channels for i in range(1024)]         #d is a  8x1024 int array
        acqs = len(d)                                   #number of acquiisitions is 1024
        self.core.reset()                               
        dev = self.sampler0                             #sets card to be run on
        dev.init()                                      #initialises sampler
        for i in range(acqs):                           #loops over number of samples
            dev.sample_mu(d[i])                         #runs sampler, saves to d
            delay(6*us)                                 #8us delay
        
        self.cb(d)                                      #move data to queue
        self.core.break_realtime()                  
