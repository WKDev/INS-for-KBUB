import serial
import pynmea2
import numpy as np
import io

#GPS Model : C94-M8P-2
GPS_PORT = '/dev/tty.usbmodem1201'
GPS_BAUD = 19200

#IMU Model : EBIMU24GV2
IMU_PORT = '/dev/tty.usbserial-0001'
IMU_BAUD = 921600


class SensorReader:
    def __init__(self, sensor_type='none'):
        print('SerialReader Started.\nWARN : It dosen\'t check the baud rate of serial device. so if data is not passed'
              ' correctly, check the baud rate')
        self.sensor_type = sensor_type
        self.imu_info = [IMU_PORT, IMU_BAUD]
        self.gps_info = [GPS_PORT, GPS_BAUD]

        self.gps = ''
        self.imu = np.array([])

        self.isIMUEnabled = False
        self.isGPSEnabled = False


        if self.sensor_type == 'imu' or self.sensor_type == 'both':
            try:
                self.ser_imu = serial.Serial(self.imu_info[0], self.imu_info[1])
                self.isIMUEnabled = self.ser_imu.readable()
                # print('imu enabled. {}   {}'.format(self.imu_info[0], self.imu_info[1]))
            except:
                print('Could not find serial port : {} for IMU. check it again.'.format(self.imu_info[0]))

        if self.sensor_type == 'gps' or self.sensor_type == 'both':
            try:
                self.ser_gps = serial.Serial(self.gps_info[0], self.gps_info[1])
                self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser_gps, self.ser_gps))

                self.isGPSEnabled = self.ser_gps.readable()
                print('gps enabled')

            except:
                print('Could not find serial port : {} for GPS. check it again.'.format(self.gps_info[0]))

        if sensor_type == 'none':
            try:
                raise ValueError('SensorReader.__init__')
            except ValueError:
                print('You should specify at least one sensor e.g. : SensorReader(type=\'imu\') ')
                raise

    # i made update_* function by mistake. this function cannot work. later, I'll find a way to use custom serialport
    # implementing argparser or txt file.
    def update_imu_info(self, port, baud):
        self.imu_info[0] = port
        self.imu_info[0] = baud

    def update_gps_info(self, port, baud):
        self.gps_info[0] = port
        self.gps_info[0] = baud

    def __sensor_connection_assertion(self, cond):
        if not cond:
            try:
                raise AssertionError('SensorReader.__init__')
            except ValueError:
                print('You should enable the sensor first before reading. ')
                raise

    def read_imu(self):

        # check if the sensor activated before read.
        self.__sensor_connection_assertion(self.isIMUEnabled)

        if self.ser_imu.readable():
            rd = self.ser_imu.readline()  # read line from serial
            rd = rd.decode()[:-2]  # remove \r\n of end of line.
            rd = rd.split(",")  # convert it str to list
            self.imu = np.array(rd)
            return self.imu
        else:
            return self.imu


    def read_gps(self):

        # check if the sensor activated before read.
        self.__sensor_connection_assertion(self.isGPSEnabled)

        if self.ser_gps.readable():
            line = self.sio.readline()  # read line from serial

            self.gps = pynmea2.parse(line)
            return self.gps

