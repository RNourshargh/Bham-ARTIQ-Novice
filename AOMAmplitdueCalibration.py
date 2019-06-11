from artiq.experiment import*
import numpy as np


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
        amps_coarse=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        amps_fine = [0.7,0.75,0.8,0.85,0.9,0.95]
        freq = 150
        attenuation= 10.0
        
        
        self.urukul0_ch0.set_att(attenuation)
        self.urukul0_ch1.set_att(attenuation)
        
        for amp in amps_coarse:
            self.urukul0_ch0.set(freq * MHz,amplitude=amp)
            self.urukul0_ch1.set(freq * MHz,amplitude=amp)
            self.urukul0_ch0.sw.on()
            self.urukul0_ch1.sw.on()
            delay(7 * s)
            self.urukul0_ch0.sw.off()
            self.urukul0_ch1.sw.off()
            delay(1*s)
            
        for amp in amps_fine:
            self.urukul0_ch0.set(freq * MHz,amplitude=amp)
            self.urukul0_ch1.set(freq * MHz,amplitude=amp)
            self.urukul0_ch0.sw.on()
            self.urukul0_ch1.sw.on()
            delay(7 * s)
            self.urukul0_ch0.sw.off()
            self.urukul0_ch1.sw.off()
            delay(1*s)