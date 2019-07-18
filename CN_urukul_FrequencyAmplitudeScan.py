from artiq.experiment import*
import numpy as np

class tutorial_urukulFreqScan(EnvExperiment):
    """Urukul Frequency & Amplitude scan"""

    def build(self):                                        #build builds channel 0 and channel 1 however output is only on channel 0
        self.setattr_device("core")
        self.setattr_device("ttl6")
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
    
    @kernel
    def run(self):
        self.core.reset()                                       #resets sinara core
        self.ttl6.output()                                      #initialises TTL channel 6, used for triggering scope
        for cpld in self.urukul_cplds:
            self.core.break_realtime()
            cpld.init()                                         #initalises all cplds

        for i in range(len(self.urukul_chs)):
            self.core.break_realtime()
            delay(10 * ms)
            self.urukul_chs[i].init()                           #initialises all urukul channels on 

        delay(100 * ms)

        for ch in self.urukul_chs:
            ch.set_att(0.0)                                     #sets all channel attenuations to 0

        delay(10 * ms)
        
        freqs_fine = [(i+1)*MHz for i in range(100)]                    #Defines frequency ramp         
        ftw_frequency = [0]*len(freqs_fine)                         #declares list for frequency tuning words (ftw)
        amplitude = [round(16383.0*(1-i/100)) for i in range(100)]   #defines list for amplitude ramp in machine units (mu)
        attenuation= 10.0                                           #defines  attenuation
        
        for i in range(len(freqs_fine)):
            ftw_frequency[i] = self.urukul0_ch0.frequency_to_ftw(freqs_fine[i]) #converts frequency list to ftw list
        
        self.core.break_realtime()                              #moves timestamp to the future
        self.urukul0_ch0.set_att(attenuation)                   #writes attenuation to urukul
        self.urukul0_ch0.sw.on()                                #switches with parallel on
        self.core.break_realtime()
        
        for i in range(len(ftw_frequency)):                     #loops length of ftw list
            with parallel:                                      
                with sequential:
                    self.urukul0_ch0.set_mu(ftw_frequency[i], asf = amplitude[i])   #sets frequency and amplitude for given list index
                    delay(10 * us)                              #minimum delay 10us for 1 channel 
                self.ttl6.pulse(1*us)                           #pulse to trigger scope

        self.urukul0_ch0.sw.off()                               #switches off urukul