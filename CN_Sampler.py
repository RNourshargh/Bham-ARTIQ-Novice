#this code reads a single value off the number of sampler channels specified with n_channels



import sys
import os
import select

from artiq.experiment import *
from artiq.coredevice.ad9910 import AD9910

if os.name == "nt":
    import msvcrt
    

class KasliTester(EnvExperiment):
    """Sampler 2kHz"""
    def build(self):
        # hack to detect artiq_run
        if self.get_device("scheduler").__class__.__name__ != "DummyScheduler":
            raise NotImplementedError(
                "must be run with artiq_run to support keyboard interaction")

        self.setattr_device("core")

        self.leds = dict()
        self.ttl_outs = dict()
        self.samplers = dict()

        ddb = self.get_device_db()
        for name, desc in ddb.items():
            if isinstance(desc, dict) and desc["type"] == "local":
                module, cls = desc["module"], desc["class"]
                if (module, cls) == ("artiq.coredevice.ttl", "TTLOut"):
                    dev = self.get_device(name)
                    if "led" in name:  # guess
                        self.leds[name] = dev
                    else:    
                        self.ttl_outs[name] = dev
                if (module, cls) == ("artiq.coredevice.sampler", "Sampler"):
                    self.samplers[name] = self.get_device(name)


        # Remove Urukul, Sampler and Zotino control signals
        # from TTL outs (tested separately)
        ddb = self.get_device_db()
        for name, desc in ddb.items():
            if isinstance(desc, dict) and desc["type"] == "local":
                module, cls = desc["module"], desc["class"]
                if (module, cls) == ("artiq.coredevice.sampler", "Sampler"):
                    cnv_device = desc["arguments"]["cnv_device"]
                    del self.ttl_outs[cnv_device]

        # Sort everything by RTIO channel number
        self.samplers = sorted(self.samplers.items(), key=lambda x: x[1].cnv.channel)

    @kernel
    def get_sampler_voltages(self, sampler, cb):
        self.core.break_realtime()      #Time break to avoid underflow condition
        sampler.init()                  #initialises sampler
        
        storage = [0.0]*200
        
        
        n_channels = 8                  #sets number of channels to read off of
                                        #change this number to alter the nummber of channels being read from          
        
        for i in range(n_channels):              #loops for each sampler channel
            sampler.set_gain_mu(i, 0)   #sets each channel's gain to 0db               
        smp = [0.0]*n_channels          #creates list of 8 floating point variables
        
        
        for n in range(200):
            delay(500*us)                       #shorter than 500us delays were causing underflow
            sampler.sample(smp)                 #runs sampler and saves to list 
            self.mutate_dataset(samples,n,smp[0])


    def run_sampler(self):                       
        for card_name, card_dev in self.samplers:   #loops over all cards on sinara device          

            #not sure what this block does but seems to be essential
            voltages = []                      
            def setv(x):                        
                nonlocal voltages               
                voltages = x  
                
            self.get_sampler_voltages(card_dev, setv)       #runs sampler function to take reading
                

    def run(self):
        self.core.reset()
        if self.samplers:
            self.run_sampler()