import numpy as np
import pyaudio

def get_pyaudio_device_indices(pa, API, input_device_name=None, output_device_name=None):
    """
    Returns a dict as:
    device['input'] = input device index
    device['output'] = output device index
    """
    host_api_dict = pa.get_host_api_info_by_type(API)
    input_device = None
    output_device = None
    
    if input_device_name:
        print("Input device: {}".format(input_device_name))
    if output_device_name:
        print("Output device: {}".format(output_device_name))
    
    
    for device_index in range(host_api_dict['deviceCount']):
        device_dict = pa.get_device_info_by_host_api_device_index(
            host_api_dict['index'],
            device_index,
        )
        if device_dict['name'] == input_device_name:
            input_device = device_dict.copy()
            print("Found specified input device (index={})".format(
                input_device['index']
            ))
        elif device_dict['name'] == output_device_name:
            output_device = device_dict.copy()
            print("Found specified output device (index={})".format(
                output_device['index']
            ))
    
    devices = dict()
    if input_device_name:
        devices['input'] = input_device['index'],
    if output_device_name:
        devices['output'] = output_device['index'],
    
    return devices

def list_all_audio_devices():
    pa = pyaudio.PyAudio()
    for id in range(pa.get_device_count()):
        dev_dict = pa.get_device_info_by_index(id)
        for key, value in dev_dict.items():
            print(key, value)
        print('\n')

class AudioStack(object):
    """
    Numpy array as a circular FIFO buffer stack.
    
    ---
    Arguments:
    n_samples_per_buffer = how many samples each buffer will hold
    n_buffer = how many buffers are in the stack

    """

    def __init__(self, n_samples_per_buffer=4800, n_buffer=100):
        self.n_samples_per_buffer = n_samples_per_buffer
        self.n_buffer = n_buffer
        self.n_samples = n_samples_per_buffer * n_buffer
        self.data = np.zeros(
            (self.n_buffer, self.n_samples_per_buffer),
            dtype=np.float32
        )
        # int keeping track of which buffer was the last to be retrieved by get_new_data
        self.last_retrieved_buffer = 0
        # int keeping track which buffers have been loaded with data
        self.elements_in_buffer = 0
        # int keeping track of which buffer to add samples to
        self.i_buffer = 0
        # array of 0 -> n_buffer
        self.indices = np.arange(self.n_buffer, dtype=np.int32)
        # int keeping track of the number of the last buffer
        self.last_buffer = np.max(self.indices)
        # array that keeps track of the real-time order of the buffers
        self.buffer_order = np.argsort(self.indices)

    def append_data(self, data_window):
        # add provided data into the correct buffer using i_buffer
        self.data[self.i_buffer, :] = data_window

        self.last_buffer += 1
        self.indices[self.i_buffer] = self.last_buffer
        self.buffer_order = np.argsort(self.indices)

        self.i_buffer += 1
        self.i_buffer = self.i_buffer % self.n_windows

        self.elements_in_buffer += 1
        self.elements_in_buffer = min(self.n_windows, self.elements_in_buffer)

    # def get_new_data(self):
    #     """
    #     Return the latest data not yet provided.
    #     """
    #     new_data = self.data[]
    #     return new_data

    # def get_most_recent(self, window_size):
    #     ordered_dataframe = np.hstack(self.data[self.buffer_order])
    #     return ordered_dataframe[self.n_samples - window_size:]

    def get_all_data(self):
        return self.data[:self.elements_in_buffer]
