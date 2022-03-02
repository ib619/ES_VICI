# Embedded Systems: Team VICI - SpikeGuard
Please visit our official website <a href = "https://vici-embedded-system.bubbleapps.io/version-test/"> here </a>.
## Participants
- Bodnar Igor (ib619)
- Bqain Issa (ib818)
- Stretcu Catalin (ms5919)
- Srivastava Varun (vs4918)

## SpikeGuard Project description
SpikeGuard is a universal lid that can protect your drink from getting spiked, it is flexible and can fit on any cup size. It uses a Raspberry Pi Zero, a pair of accelerometers and an app built on the kivy framework in order to notify the user if their drink has been tampered with. All of the accelerometer data is processed on the Raspberry Pi and important messages are sent to the app via MQTT. The repo contains the code for both the data processing scripts that run on the Raspberry Pi and for the Kivy app, as well as some Python scripts used for the testing of MQTT communication and sensor event detection. Observe below the dependencies, instructions and features of this project.

### Installing Dependencies
```
pip install paho-mqtt
pip install numpy
pip install GPIO
pip install smbus2
pip install ssl
pip install urllib
pip install matplotlib
pip install kivy[base]
```

### Program Execution
```
python main.py 
python device_main_final.py
```

## Features and Connectivity
In addition to the secure MQTT protocol for communication between your device and the Pi, a few advanced features are added to ensure accurate and efficient transfer of data from the sensors and to improve user experience.
### Sensor data 
Two accelerometer are placed diagonally opposite each other with opposite XYZ frame assignments. Their differential input is used to detect changes in movements of the lid. In addition tilt angles are caluculated to detect any "lifting" or "bending" of the flexible lid in spike event detection.
### Filtering input sensor data
A moving average filter is used to remove high frequency noise from the sensor data.
### Loosing connection to your device and reconnecting
In the case that a user moves to an area where they are not able to connect to their device, the device will detect a loss of connection and begin to store event data locally. Once the connection is re-established, the device will update the user if there where any drink spike events detected through the app.
### Secure MQTT broker
Hosting an MQTT broker on an ubuntu AWS vitual machine using using AWS E2C instance. Port 1883 and port 8884 are available, port 8884 requires an SSL certificate and key for an encrypted connection with client authentication.
### Spike Event Detection
In a Spike event detection cycle where counter = N, 10 in this case, must obtain M or more Spikes, 8 in this case, to alert user of a Spike event detection. Spikes are detected using changes in differential X,Y,Z positions aswell as the tilt angles in X and Y direction (tilt in Z represents the lid spinning and has not proven useful).

Event detection, cycle period and spike detection threshold values are tuned to remain very sensetive to any changes in lid movements but not simple vibrations or movements which would send a fale positiive event detection. False Nngatives are unacceptable given the usecase of the device and hence the threshold values have been calibrated to prevent this from happening

## App
#### Running the script
1. Install the following libraries:
	* kivy
	* paho-mqtt
2. Run **main.py** using Python 3

#### UI
1. Left screen is used to connect to MQTT from the app.
2. Right screen is used to arm/disarm the device.


# Testing Accelerometers
### Raspberry Pi
#### Overview
The script configures the acceletrometer to collect data at 10Hz rate continuously with range +/-2G.
Due to the restrictions on message rate on public MQTT brockers it sends data via MQTT in large packets.
The measurements are being passed through a moving average filter to remove some noise from the signal.

#### Running the script
1. Install the following libraries
	* smbus2
	* paho-mqtt
2. Run **raspi_plot_acc.py**
3. The script operation can be changed via altering constants inside **raspi_plot_acc.py**
	* **MEASURE_INTERVAL** sets the measurement period in seconds (default = 0.1)
	* **FILTER_WINDOW_SIZE** sets the buffer lenght for a moving average filter (default = 4)
	* **PACKET_SIZE** sets the number of measurements in a packet (default = 16)
	* **NUMBER_OF_PACKETS** sets the total number of packets to be sent to PC (default = 6)
	* **REMOVE_GRAVITY_OFFSET** removes 1G offset due to gravity from Z-Axis measurement (default = True)

### PC
#### Overview
The script uses multithreading to continuously receive data from Raspberry Pi via MQTT and plot the data in real time.

#### Running the script
1. Install the following libraries:
	* paho-mqtt
	* matplotlib
2. Run **pc_plot_acc.py**
3. The script operation can be changed via altering constants inside **pc_plot_acc.py**
	* **ACCEL_AXIS_MIN** sets the minimum value on the acceleration axis (default -1.5)
	* **ACCEL_AXIS_MAX** sets the maximum value on the acceleration axis (default 1.5)
