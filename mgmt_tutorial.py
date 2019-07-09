from artiq.experiment import *
import time
import numpy as np


class MgmtTutorial(EnvExperiment):
    """Management tutorial"""
    def build(self):
        self.setattr_argument("count", NumberValue(ndecimals=0, step=1))

    def run(self):
        self.set_dataset("parabola", np.full(self.count, np.nan), broadcast=True)
        for i in range(self.count):
            self.mutate_dataset("parabola", i, i*i)
            time.sleep(0.5)