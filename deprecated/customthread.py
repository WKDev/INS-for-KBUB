## DEPRECATED_Mar18, 2022

## data_fetcher.py
# fetches data from GPS and IMU
# Version 1.0.0 | First Creation
# Version 1.0.1 | Organized functions into one class
# Created : Chanhhyeok Son
# Date : Mar 14, 2022


import threading
import serial, signal
import pynmea2
from queue import Queue
#GPS Model : C94-M8P-2
GPS_PORT = '/dev/cu.usbmodem11201'
GPS_BAUD = 19200

#IMU Model : EBIMU24GV2
IMU_PORT = '/dev/tty.usbserial-0001'
IMU_BAUD = 921600

class FetchINSData:
    def __init__(self, mode = 'GPS', print_data = True, port = '/dev/tty.usbserial-0001', baud = 921600):
        self.mode = mode # select which to read
        self.ser = None # serial class
        self.print_data = print_data # set to True to print data
        self.line = [] # temporarily saves data to here.
        self.exitcode = False # exitcode to terminate thread
        self.thread = None # thread class
        self.serial_data = None # processed data
        self.q = Queue(maxsize = 500)

    # 쓰레드 종료용 시그널 함수
    def handler(self, signum, frame):
        self.exitcode = True

    # 데이터 처리할 함수
    def print(self, data):

        if self.mode == 'IMU':
            # print("Q1 : {} | Q2 : {} | Q3 : {} | IMU Battery Level : {}%".format(tmp_list[1], tmp_list[2], tmp_list[3],tmp_list[4][:2]))
            print('test')
        elif self.mode == 'GPS':
            msg = pynmea2.parse(data)

            print(msg)


    def readThread(self,ser = None, line = [], exitcode = False):

        self.line = line
        # 쓰레드 종료될때까지 계속 돌림
        while not exitcode:
            # 데이터가 있있다면
            for c in ser.read():
                # line 변수에 차곡차곡 추가하여 넣는다.
                self.line.append(chr(c))

                if c == 10:  # 라인의 끝을 만나면
                    tmp = ''.join(self.line)  # list -->String
                    tmp_list = tmp.split(",")
                    if tmp_list is not None and len(tmp_list) == 5:
                        imu_data = {'x': tmp_list[1], 'y': tmp_list[2], 'z': tmp_list[3],
                                'batt_level': tmp_list[4][:2]}
                        self.q.put(imu_data)

                    # 데이터 처리 함수로 호출
                    if self.print_data:
                        self.print(self.line)
                    # line 변수 초기화
                    del self.line[:]

    def init_thread(self):
        #exit code 등록
        signal.signal(signal.SIGINT, self.handler)
        # 스레드 생성
        self.thread = threading.Thread(target=self.readThread, args=(self.ser, self.line, self.exitcode))

    def init_serial(self):
        if self.mode == 'IMU':
            print("Serial Initialization | type : {} , Target_Port : {}, Baud_rate : {}".format(self.mode, IMU_PORT, IMU_BAUD))

            try:
                self.ser = serial.Serial(IMU_PORT, IMU_BAUD, timeout=0)
            except:
                print('Could not find serial port : {} for IMU. check it again.'.format(IMU_PORT))

        elif self.mode == 'GPS':
            print("Serial Initialization | type : {} , Target_Port : {}, Baud_rate : {}".format(self.mode, GPS_PORT, GPS_BAUD))

            try:
                self.ser = serial.Serial(GPS_PORT, GPS_BAUD, timeout=0)
            except:
                print('Could not find serial port : {} for GPS. check it again.'.format(GPS_PORT))


    def get_imu_data(self):
            return self.q.get()

        # return self.serial_data

    def start(self):
        self.thread.start()






