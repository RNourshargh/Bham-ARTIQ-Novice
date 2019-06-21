from artiq.experiment import*


def input_led_state() -> TBool: #This defines a function that returns a boolian variable. The input is read from the command line and returned.
    return input("Enter desired LED state: ") == "1"
	
class tutorial_LEDKeyedInput(EnvExperiment):
    """Tutorial: LED keyed input"""
	def build(self):
        #This sets the device drivers as attributes and adds the key to the kernel invarients (things stored on the FPGA). You have to do this to use the device 
		self.setattr_device("core")
		self.setattr_device("led0")
		self.setattr_device("led1")
	@kernel #This decorator tells the system to run the following code on the core device (FPGA) rather than to run it as normal python code on the host (computer)
	def run(self):
		self.core.reset()
		s = input_led_state() #Call the function defined earlier and store the output as "s"
		self.core.break_realtime() #This moves the timeline far enough into the future to ensure that the input has been entered before the system tries to check the condition
		if s:
			self.led0.on() #switch on the LED
			self.led1.on()
		else:
			self.led0.off() #switch off the LED
			self.led1.off()