import nidaqmx
from nidaqmx import constants
from nidaqmx import system

"""
sys = nidaqmx.system.System.local()  # load local system

task_names = sys.tasks.task_names  # returns a list of task names

task = sys.tasks[0]  # selected the first task
"""

loaded_task = nidaqmx.Task()

sent_samples = []  # list for saving acquired data

loaded_task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
loaded_task.timing.cfg_samp_clk_timing(
    rate=2560,
    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
    samps_per_chan=1000)


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

# input('Running task. Press Enter to stop.\n')
