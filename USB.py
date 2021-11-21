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
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            task.timing.cfg_samp_clk_timing(self.sampleRate, sample_mode=constants.AcquisitionType.CONTINUOUS,
                                            samps_per_chan=(self.sampleRate * self.sampleTime))

            samples_per_buffer = int(self.sampleRate // 30)  # 30 hz update
            reader = stream_readers.AnalogMultiChannelReader(task.in_stream)
            writer = stream_writers.AnalogMultiChannelWriter(task.out_stream)

            def reading_task_callback(task_idx, event_type, num_samples, callback_data=None):
                num_channels = 1
                print(num_samples)
                buffer = np.zeros(num_samples, dtype=np.float32)
                reader.read_many_sample(buffer, num_samples, timeout=constants.WAIT_INFINITELY)
                print(buffer)

                # Convert the data from channel as a row order to channel as a column
                data = buffer.T.astype(self.dtype)
                print(data)

            task.register_every_n_samples_acquired_into_buffer_event(samples_per_buffer, reading_task_callback)

    def sample2(self):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            task.timing.cfg_samp_clk_timing(self.sampleRate, sample_mode=constants.AcquisitionType.CONTINUOUS,
                                            samps_per_chan=(self.sampleRate * self.sampleTime))
            sent_samples = []

            def callback(task_handle, every_n_samples_event_type,
                         number_of_samples, callback_data):
                """
                Callback function/
                """
                print('Every N Samples callback invoked.')

                samples = task.read(number_of_samples_per_channel=200)
                sent_samples.extend(samples)

                return 0
            task.register_every_n_samples_acquired_into_buffer_event(200, callback)
            task.start()

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
