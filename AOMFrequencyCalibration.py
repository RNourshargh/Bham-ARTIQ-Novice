from artiq.experiment import*
import numpy as np

def input_keystroke() -> TBool:
    return input("Press enter to move to the next value") == "1"

class DDS(EnvExperiment):
    def build(self):
        self.setattr_device("core")

        urukuls = [
            "urukul0", "urukul1"
        ]

        self.urukul_cplds = [self.get_device(name + "_cpld") for name in urukuls]
        self.urukul_chs = [
            self.get_device(name + "_ch{}".format(i)) for i in range(4)
            for name in urukuls
        ]
        
        devs = [
        "urukul0_ch0",
        "urukul0_ch1",
        ]

        
        for dev in devs:
            self.setattr_device(dev)

        #self.ttl_outputs = [self.get_device("ttlo{}".format(i)) for i in range(4)]
    
    @kernel
    def run(self):
        self.core.reset()
        
        for cpld in self.urukul_cplds:
            self.core.break_realtime()
            cpld.init()

        for i in range(len(self.urukul_chs)):
            self.core.break_realtime()
            delay(10 * ms)
            self.urukul_chs[i].init()

        delay(100 * ms)

        for ch in self.urukul_chs:
            ch.set_att(0.0)

        delay(10 * ms)
        
        """Adjustable parameters"""
        freqs_coarse=[130,135,140,145,150,155,160,165]
        freqs_fine = [148.0,148.5,149.0,149.5,150.0,150.5,151.0,151.5,152.,152.5,153.]
        amp=0.9
        attenuation= 10.0
        
        
        self.urukul0_ch0.set_att(attenuation)
        self.urukul0_ch1.set_att(attenuation)
        
        for freq in freqs_coarse:
            self.urukul0_ch0.set(freq * MHz,amplitude=amp)
            self.urukul0_ch1.set(freq * MHz,amplitude=amp)
            self.urukul0_ch0.sw.on()
            self.urukul0_ch1.sw.on()
            delay(7 * s)
            self.urukul0_ch0.sw.off()
            self.urukul0_ch1.sw.off()
            delay(1*s)
            
            
        for freq_float in freqs_fine:
            self.urukul0_ch0.set(freq_float * MHz,amplitude=amp)
            self.urukul0_ch1.set(freq_float * MHz,amplitude=amp)
            self.urukul0_ch0.sw.on()
            self.urukul0_ch1.sw.on()
            delay(7 * s)
            self.urukul0_ch0.sw.off()
            self.urukul0_ch1.sw.off()
            delay(1*s)