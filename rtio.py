from artiq.experiment import *



class Tutorial(EnvExperiment):
    def build(self):
        j = 22
        self.setattr_device("core")
        self.setattr_device("ttl6")
        self.setattr_device("ttl"+str(j))
        self.setattr_device("ttl"+str(j+1))
        
    @kernel
    def run(self):
        self.core.reset()
        self.ttl6.output()
        self.ttl22.output()
        self.ttl23.output()
        
        for i in range(1000000):
            delay(2*us)
            with parallel:
                self.ttl6.pulse(2*us)
                with sequential:
                    self.ttl22.pulse(2*us)
                    delay(1*us)
                    self.ttl23.pulse(1*us)

        for i in range(1000000):
            delay(2*us)
            with parallel:
                self.ttl6.pulse(2*us)
                self.ttl23.pulse(2*us)