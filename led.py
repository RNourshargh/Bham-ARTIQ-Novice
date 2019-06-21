from artiq.experiment import*


def input_led_state() -> TBool: #This defines a function that returns a boolian variable. The input is read from the command line and returned.
    return input("Enter desired LED state: ") == "1"
	
class LED(EnvExperiment):
	def build(self):
        #This sets the device drivers as attributes and adds the key to the kernel invarients (things stored on the FPGA). You have to do this to use the device 
		self.setattr_device("core")
		self.setattr_device("led0")
		self.setattr_device("led1")
	@kernel
	def run(self):
		self.core.reset()
		s = input_led_state() #Call the function defined earlier and store the output as "s"
		self.core.break_realtime() #I don't fully understand how this works but functionally it lets the system wait for an input before resuming real time operation
		if s:
			self.led0.on() #switch on the LEDs
			self.led1.on()
		else:
			self.led0.off() #switch off the LEDs
			self.led1.off()