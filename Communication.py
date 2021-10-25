import nidaqmx
import pprint
import numpy as np
from matplotlib import pyplot as plt

pp = pprint.PrettyPrinter(indent=4)


class USB(object):
    def __init__(self):
        super().__init__()
        self.data = 0
        self.dataStr = ""

    def read(self):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")

            print('1 Channel 1 Sample Read: ')
            self.data = task.read()
            pp.pprint(self.data)
            self.data = round(self.data, 2)
            self.dataStr = str(self.data)
"""
            data = task.read(number_of_samples_per_channel=1)
            pp.pprint(data)

            print('1 Channel N Samples Read: ')
            data = task.read(number_of_samples_per_channel=10)
            x = np.arange(0, len(data))
            pp.pprint(data)
            plt.plot(x, data)

            task.ai_channels.add_ai_voltage_chan("Dev1/ai1")

            print('N Channel 1 Sample Read: ')
            data = task.read()
            pp.pprint(data)

            print('N Channel N Samples Read: ')
            data = task.read(number_of_samples_per_channel=2)
            pp.pprint(data)
"""

