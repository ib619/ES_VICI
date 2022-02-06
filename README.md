# Embedded Systems: Team VICI

## Participants
- Bodnar Igor (ib619)
- Bqain Issa (ib818)
- Stretcu Catalin (ms5919)
- Srivastava Varun (vs4918)

## Plotting Accelerometer Data

### Raspberry Pi
1. Install the following libraries
	* smbus2
	* paho-mqtt
2. Run **raspi_plot_acc.py**
3. The script operation can be changed via altering constants inside **raspi_plot_acc.py**
	* **MEASURE_INTERVAL** sets the measurement period in seconds (default = 0.1)
	* **FILTER_WINDOW_SIZE** sets the buffer lenght for a moving average filter (default = 16)
	* **PACKET_SIZE** sets the number of measurements in a packet (default = 16)
	* **NUMBER_OF_PACKETS** sets the total number of packets to be sent to PC (default = 6)
	* **REMOVE_GRAVITY_OFFSET** removes 1g offset due to gravity from Z-Axis measurement (default = 0.1)