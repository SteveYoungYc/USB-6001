import nidaqmx
import pprint
import numpy as np
from matplotlib import pyplot as plt
from nidaqmx import constants
from nidaqmx import stream_readers
from nidaqmx import stream_writers

pp = pprint.PrettyPrinter(indent=4)


class USB(object):
    def __init__(self):
        super().__init__()
        self.data = 0
        self.dataStr = ""
        self.output = 1
        self.x = 0
        self.y = 0
        self.sampleRate = 10000
        self.sampleTime = 2
        self.task = nidaqmx.Task()
        self.samples = []
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        self.task.timing.cfg_samp_clk_timing(
            rate=self.sampleRate,
            sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
            samps_per_chan=self.sampleRate * self.sampleTime)

    def read(self):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")

            # print('1 Channel 1 Sample Read: ')
            self.data = task.read()
            # pp.pprint(self.data)
            self.data = round(self.data, 4)
            self.dataStr = str(self.data)

            data = task.read(number_of_samples_per_channel=10)
            self.x = np.arange(0, len(data))
            self.y = data

    def write(self, writeData):
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
            task.write(writeData)
            # task.timing.cfg_samp_clk_timing()

    def sample(self):
        loaded_task = nidaqmx.Task()

        sent_samples = []  # list for saving acquired data

        loaded_task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        loaded_task.timing.cfg_samp_clk_timing(
            rate=self.sampleRate,
            sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
            samps_per_chan=self.sampleRate * self.sampleTime)

        def callback(task_handle, every_n_samples_event_type,
                     number_of_samples, callback_data):
            """
            Callback function/
            """
            print('Every N Samples callback invoked.')

            samples = loaded_task.read(number_of_samples_per_channel=2560)
            sent_samples.extend(samples)
            print(samples)
            return 0

        loaded_task.register_every_n_samples_acquired_into_buffer_event(200, callback)

        loaded_task.start()

