from artiq.experiment import*

class LED(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("led0")
        self.setattr_device("led1")
    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()

        for i in range(10):    
            for i in range(5):
                delay(300*ms)
                with parallel:
                    self.led0.pulse(300*ms)
                    self.led1.pulse(300*ms)
                
                for i in range(2):
                    self.led0.pulse(300*ms)
                    self.led1.pulse(300*ms)