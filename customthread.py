import threading
import serial, signal
import pynmea2

#GPS Model : C94-M8P-2
GPS_PORT = '/dev/cu.usbmodem1201'
GPS_BAUD = 19200

#IMU Model : EBIMU24GV2
IMU_PORT = '/dev/tty.usbserial-0001'
IMU_BAUD = 921600

class FetchINSData:
    def __init__(self, mode = 'GPS', print_data = True):
        self.mode = mode
        self.ser = None
        self.print_data = print_data
        self.line = []
        self.exitcode = False
        self.thread = None

    # 쓰레드 종료용 시그널 함수
    def handler(self, signum, frame):
        self.exitcode = True

    # 데이터 처리할 함수
    def print(self, data):
        tmp = ''.join(data) # list -->String
        tmp_list = tmp.split(",") # split String by ',' and save it to list

        if self.mode == 'IMU':
            print("Q1 : {} | Q2 : {} | Q3 : {} | IMU Battery Level : {}%".format(tmp_list[1], tmp_list[2], tmp_list[3],tmp_list[4][:2]))
        elif self.mode == 'GPS':
            msg = pynmea2.parse(tmp)

            print(msg)


    def readThread(self,ser = None, line = [], exitcode = False):

        self.line = line
        # 쓰레드 종료될때까지 계속 돌림
        while not exitcode:
            # 데이터가 있있다면
            for c in ser.read():
                # line 변수에 차곡차곡 추가하여 넣는다.
                self.line.append(chr(c))

                if c == 10:  # 라인의 끝을 만나면..
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
            self.ser = serial.Serial(IMU_PORT, IMU_BAUD, timeout=0)
            print("Serial Initialization | type : {} , Target_Port : {}, Baud_rate : {}".format(self.mode, IMU_PORT, IMU_BAUD))

        elif self.mode == 'GPS':
            self.ser = serial.Serial(GPS_PORT, GPS_BAUD, timeout=0)
            print("Serial Initialization | type : {} , Target_Port : {}, Baud_rate : {}".format(self.mode, GPS_PORT, GPS_BAUD))



    def start(self):
        self.thread.start()






