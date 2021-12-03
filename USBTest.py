import sys

import nidaqmx
from PyQt5.QtWidgets import QApplication
from nidaqmx import constants
from nidaqmx import system

from MainWindow import Ui_MainWindow
from PyQtTest import MyGraphWindow
import time

"""
sys = nidaqmx.system.System.local()  # load local system

task_names = sys.tasks.task_names  # returns a list of task names

task = sys.tasks[0]  # selected the first task
"""

SAMPLES_NUM = 50000

time_start = time.time()
time_end = time.time()
loaded_task = nidaqmx.Task()

USB_samples = []  # list for saving acquired data
x = range(0, SAMPLES_NUM)

loaded_task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
loaded_task.timing.cfg_samp_clk_timing(rate=10000,
                                       sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                       samps_per_chan=20000)


def callback(task_handle, every_n_samples_event_type,
             number_of_samples, callback_data):
    """
    Callback function/
    """
    print('Every N Samples callback invoked.')
    start_time = time.time()

    samples = loaded_task.read(number_of_samples_per_channel=SAMPLES_NUM)
    USB_samples.extend(samples)
    print(len(USB_samples))
    # print(sent_samples)
    end_time = time.time()
    print(end_time - start_time)
    loaded_task.close()

    app = QApplication(sys.argv)
    my_window = MyGraphWindow()
    my_window.show()
    my_window.plot(x, USB_samples)
    sys.exit(app.exec_())


loaded_task.register_every_n_samples_acquired_into_buffer_event(200, callback)

with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
    task.write(3.3)
loaded_task.start()

# input('Running task. Press Enter to stop.\n')
