# Bluetooth Wearable Device Dataset
This repository contains metadata and usage examples of radio recordings from wearable devices, captured using SDR in an RF isolated environment. The raw data recordings can be accessed from ... . Each recording is accompanied by its own metadata file (top.yaml), detailing its production process and parameters.

You can find example radio recording in the _example_radio_data/ folder.

## Example usage
```
pip3 install -r requirements.txt
python3 plot_data.py /path/to/top.yaml
```
```console
python3 plot_data.py _example_radio_data/top.yaml 
Choose a file to load:
1. Channels_05 data (Channelized 5 MHz Bandwidth)
2. Channels_25 data (Channelized 25 MHz Bandwidth)
3. Output Recording (Not Channelized)
Enter the number corresponding to the file you want to load: 3
Data From _example_radio_data/./radio.data loaded.
Sample Rate: 100000000
Center Frequency: 2441500000
Recording Duration: 0.003 seconds
BD_ADDR of Wearable Device: None
Connection Timestamps:
- Enabling bluetooth on smartphone: None seconds
- Disconnected: None seconds
Enter the start time (in seconds): 0
Enter the stop time (in seconds): 0.003
```

PICTURE HERE

## Metadata structure

### Recording Details

- **Recording Date:** Date of the recording.
- **Recording Location:** Location where the recording took place.

#### Recording Device

- Details about the recording device used for recording, tuned frequency, gain settings and output file.

#### Wearable Device

- Information about the wearable device being recorded. Device type, Bluetooth address and applications used.

#### Master Device

- Details about the master device involved in the recording. 

### Recording Duration

- Duration of the recording in seconds.

### Recording Timeline Description

- Timestamps of specific events during the recording process. 

### Event Scenario

- Whether or not the Wearable device was paired to Master Device before the recording.

### Event Desription

- Description of events that occurred during the recording.

### File Format

- Format of the recorded data files.

### Channelized Data

- Information about the channelized data. 