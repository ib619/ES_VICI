# Embedded Systems: Team VICI

## Participants
- Bodnar Igor (ib619)
- Bqain Issa (ib818)
- Stretcu Catalin (ms5919)
- Srivastava Varun (vs4918)

## Plotting Accelerometer Data

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
	* **FILTER_WINDOW_SIZE** sets the buffer lenght for a moving average filter (default = 16)
	* **PACKET_SIZE** sets the number of measurements in a packet (default = 16)
	* **NUMBER_OF_PACKETS** sets the total number of packets to be sent to PC (default = 6)
	* **REMOVE_GRAVITY_OFFSET** removes 1G offset due to gravity from Z-Axis measurement (default = True)

### PC
#### Overview
The script uses multithreading to continuously receive data from Raspberry Pi via MQTT and plot the data in real time.

#### Running the script
1. Install the following libraries
	* paho-mqtt
	* matplotlib
2. Run **pc_plot_acc.py**
3. The script operation can be changed via altering constants inside **pc_plot_acc.py**
	* **ACCEL_AXIS_MIN** sets the minimum value on the acceleration axis (default -1.5)
	* **ACCEL_AXIS_MAX** sets the maximum value on the acceleration axis (default 1.5)



### Advanced features
In addition to the secure MQTT protocol for communication between your device and the Pi, a few advanced features are added to ensure accurate and efficient transfer of data from the sensors and to improve user experience.

#### Filtering input sensor data
A moving average filter is used to remove high frequency noise from the sensor data. 
#### Loosing connection to your device and reconnecting
In the case that a user moves to an area where they are not able to connect to their device, the device will detect a loss of connection and begin to store event data locally. Once the connection is re-established, the device will update the user if there where any drink spike events detected.
#### Push notifications to alert of a possible spike event
