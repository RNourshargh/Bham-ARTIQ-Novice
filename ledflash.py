from artiq.experiment import*

class LEDrealTime(EnvExperiment):
    def build(self): #Adds the device drivers as attributes and adds the keys to the kernel invarients
        self.setattr_device("core")
        self.setattr_device("led0")
        self.setattr_device("led1")
    @kernel #Tells the system to run the following on the core device
    def run(self):
        self.core.reset()
        for i in range(10):    
            for i in range(5):
                delay(300*ms)
                with parallel: #These events happen simultaneously
                    self.led0.pulse(300*ms)
                    self.led1.pulse(300*ms)
                
                for i in range(2): #These events happen sequentially
                    self.led0.pulse(300*ms)
                    self.led1.pulse(300*ms)