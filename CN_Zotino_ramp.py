from artiq.experiment import *

class ZotinoOutputs(EnvExperiment):
    """Zotino: Ramp Generator"""
    def build(self): 

        self.setattr_device("core")
        self.setattr_device("zotino0")

    @kernel
    def set_zotino_voltages(self, zotino, voltages):
        self.core.break_realtime()                          #puts timestamp in future
        zotino.init()                                       #initialises zotino
        delay(200*us)                                       #allows initialisation to finnish

        while(1):                                           #loops until manually broken
            for voltage in voltages:                        #loops over all voltages in voltage list
                    
                zotino.write_dac_mu(0, voltage)             #writes voltages as machine units to output channel buffer register
                zotino.load()                               #loads buffer to output
                
                delay(800*ns)                               #800ns delay minimum for 1 channel, 2us minimum for 2 channels
                
    def test_zotinos(self):#
        n_steps = 100                                       #number of steps into which ramp will be broken
        voltages_mu = [((1<<16)//n_steps)*i                 #defines voltage ramp in machine units, 0.2V steps from -10V to 10V
            for i in range(n_steps)]
           
        self.set_zotino_voltages(self.zotino0, voltages_mu)    #runs set voltages code

    def run(self):
        self.core.reset()
        self.test_zotinos()
        
    