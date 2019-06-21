from artiq.experiment import*


class tutorial_UrukulOn(EnvExperiment):
    """Tutorial: Ururkul On"""
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
        
        a = self.urukul0_ch1.frequency_to_ftw(100*MHz)
        b = self.urukul0_ch1.frequency_to_ftw(200*MHz)
        
        print("FTW for 100MHz is:",a)
        print("FTW for 200MHz is:",b)
        
        phase_mu = 0 
        pow_pi2 = self.urukul0_ch1.turns_to_pow(0.25)
        print("POW for pi phase is:", pow_pi2)
        
        
        self.urukul0_ch0.set(200 * MHz,amplitude=0.9)
        self.urukul0_ch0.set_mu(2*a)
        self.urukul0_ch0.set_att(0.)
        
        self.urukul0_ch1.set(100 * MHz, phase =0.0, amplitude=0.9)
        #self.urukul0_ch1.set_mu(a,phase_mu+pow_pi2)
        self.urukul0_ch1.set_att(0.)
        
        self.urukul0_ch0.sw.on()
        self.urukul0_ch1.sw.on()
        
       