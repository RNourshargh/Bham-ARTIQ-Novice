from artiq.experiment import*


def input_led_state() -> TBool:
    return input("Enter desired LED state: ") == "1"
	
class LED(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("led0")
		self.setattr_device("led1")
	@kernel
	def run(self):
		self.core.reset()
		s = input_led_state()
		self.core.break_realtime()
		if s:
			self.led0.on()
			self.led1.on()
		else:
			self.led0.off()
			self.led1.off()