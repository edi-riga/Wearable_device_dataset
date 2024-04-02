import yaml
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def load_data_from_file(file_path, file_format, sample_rate):
    return np.fromfile(file_path, dtype=file_format), sample_rate

def draw_waveform(data, sample_rate, file_path, start_time):
    # Generate time axis based on sample rate and data length
    time_axis = np.arange(start_time, start_time + len(data) / sample_rate, 1 / sample_rate)[:len(data)]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(time_axis, np.real(data))  # Assuming complex data; you can modify this based on your data type
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Amplitude')
    ax.grid()
    ax.set_title("Waveform")
    # plt.title(f'Waveform - {file_path}')

def draw_fft(data, sample_rate, file_path, center_frequency):
    fft_result = np.fft.fft(data)
    freq_axis = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
    freq_axis_shifted = freq_axis + center_frequency
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(freq_axis_shifted, np.abs(fft_result))
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude (dB)')
    ax.grid()
    ax.set_title("FFT")
    # ax.set_title(f'FFT - {file_path}')

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 plot_data.py <metadata_file>")
        sys.exit(1)

    yaml_file_path = sys.argv[1]

    # Load YAML data from file
    with open(yaml_file_path, 'r') as file:
        metadata = yaml.safe_load(file)

    # Extract channelized data information
    channelized_data = metadata['channelized_data']
    channelized_data_05 = channelized_data['channels_05']
    channelized_data_25 = channelized_data['channels_25']
    output_file_path = metadata['recording_device']['output_file']

    # Prompt user for file loading options
    print("Choose a file to load:")
    print("1. Channels_05 data (Channelized 5 MHz Bandwidth)")
    print("2. Channels_25 data (Channelized 25 MHz Bandwidth)")
    print("3. Output Recording (Not Channelized)")
    option = int(input("Enter the number corresponding to the file you want to load: "))

    if option == 1:
        # Prompt the user to choose a file for channels_05
        print("\nChoose a file for channels_05:")
        for idx, file_path in enumerate(channelized_data_05['output_file_ch05']):
            print(f"{idx + 1}. {file_path}")

        selected_idx = int(input("Enter the number corresponding to the file you want to load: ")) - 1
        selected_file = channelized_data_05['output_file_ch05'][selected_idx]
        file_format = metadata['file_format']
        if file_format.startswith('numpy.'):
            selected_dtype = np.dtype(file_format.split('.', 1)[1])
        else:
            print("Invalid file format. Exiting.")
            sys.exit(1)
        selected_sample_rate = channelized_data_05['sample_rate_ch05']
        selected_center_frequency = channelized_data_05['center_frequency_ch05'][selected_idx]  # Added this line
    elif option == 2:
        # Prompt the user to choose a file for channels_25
        print("\nChoose a file for channels_25:")
        for idx, file_path in enumerate(channelized_data_25['output_file_ch25']):
            print(f"{idx + 1}. {file_path}")

        selected_idx = int(input("Enter the number corresponding to the file you want to load: ")) - 1
        selected_file = channelized_data_25['output_file_ch25'][selected_idx]
        file_format = metadata['file_format']
        if file_format.startswith('numpy.'):
            selected_dtype = np.dtype(file_format.split('.', 1)[1])
        else:
            print("Invalid file format. Exiting.")
            sys.exit(1)
        selected_sample_rate = channelized_data_25['sample_rate_ch25']
        selected_center_frequency = channelized_data_25['center_frequency_ch25'][selected_idx]  # Added this line
    elif option == 3:
        selected_file = output_file_path
        file_format = metadata['file_format']
        if file_format.startswith('numpy.'):
            selected_dtype = np.dtype(file_format.split('.', 1)[1])
        else:
            print("Invalid file format. Exiting.")
            sys.exit(1)
        selected_sample_rate = metadata['recording_device']['sample_rate']
        selected_center_frequency = metadata['recording_device']['center_frequency']  # Added this line
    else:
        print("Invalid option. Exiting.")
        sys.exit(1)

    full_file_path = os.path.join(os.path.dirname(yaml_file_path), selected_file)

    try:
        loaded_data, sample_rate = load_data_from_file(full_file_path, selected_dtype, selected_sample_rate)
        print(f"Data From {full_file_path} loaded.")
        print(f"Sample Rate: {sample_rate}")
        print(f"Center Frequency: {selected_center_frequency}")
        print(f"Recording Duration: {metadata['recording_duration_seconds']} seconds")
        print(f"BD_ADDR of Wearable Device: {metadata['wearable_device']['BD_ADDR']}")
        print("Connection Timestamps:")
        for event, timestamp in metadata['recording_timeline_description'].items():
            print(f"- {event.replace('_', ' ').capitalize()}: {timestamp} seconds")
            
        # Prompt the user for start and stop times
        start_time = float(input("Enter the start time (in seconds): ").strip())
        stop_time = float(input("Enter the stop time (in seconds): ").strip())
        start_index = int(start_time * sample_rate)
        stop_index = int(stop_time * sample_rate)

        if start_time >= stop_time:
            print("Error: Start time must be less than stop time.")
            sys.exit(1)

        draw_waveform(loaded_data[start_index:stop_index], sample_rate, full_file_path, start_time)
        draw_fft(loaded_data[start_index:stop_index], sample_rate, full_file_path, selected_center_frequency)
        plt.show()
    except FileNotFoundError:
        print(f"Error: {full_file_path} not found. Please check the file path and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
