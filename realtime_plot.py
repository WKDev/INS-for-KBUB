import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import serial

# GPS Model : C94-M8P-2
GPS_PORT = '/dev/cu.usbmodem11201'
GPS_BAUD = 19200

# IMU Model : EBIMU24GV2
IMU_PORT = '/dev/tty.usbserial-0001'
IMU_BAUD = 921600

# x_limit of plots
X_LENGTH = 50

# update interval of animated plots
INTERVAL = 1

class RTPlot:  # RTPlot animates the movement of imu.

    def __init__(self):

        self.pitch_array = np.empty((0, 2), float)
        self.roll_array = np.empty((0, 2), float)
        self.yaw_array = np.empty((0, 2), float)

        self.fig = plt.figure()
        self.fig, axs = plt.subplots(3, sharex=True, sharey=True)
        self.fig.suptitle('IMU')

        axs[0].set_xlim([0, X_LENGTH])
        axs[0].set_ylim([-180, 180])
        axs[0].set_title('Pitch')
        axs[1].set_xlim([0, X_LENGTH])
        axs[1].set_ylim([-180, 180])
        axs[1].set_title('Roll')

        axs[2].set_xlim([0, X_LENGTH])
        axs[2].set_ylim([-180, 180])
        axs[2].set_title('Yaw')

        self.line_p, = axs[0].plot([], [], lw=2,color='limegreen')
        self.line_r, = axs[1].plot([], [], lw=2, color='red')
        self.line_y, = axs[2].plot([], [], lw=2)
        self.ser = serial.Serial(IMU_PORT,IMU_BAUD)

        self.curr_data = self.get_imu()

        # TBD : performance issue should be resolved.
        # self.p_txt = plt.text(0, 0, ' ', ha='center', va='center', fontsize=20, color="Red")
        # self.r_txt = axs[1].text(0, 0, ' ', ha='center', va='center', fontsize=20, color="Red")
        # self.y_txt = axs[2].text(0, 0, ' ', ha='center', va='center', fontsize=20, color="Red")
        #


    def get_imu(self):
        if self.ser.readable():
            rd = self.ser.readline()  # read line from serial
            rd = rd.decode()[:-2]  # remove \r\n of end of line.
            rd = rd.split(",")  # convert it str to list
            rd = np.array(rd)
            return rd

    # init every line
    def init_y(self):
        self.line_y.set_data([], [])
        return self.line_y,

    def init_p(self):
        self.line_p.set_data([], [])
        return self.line_p,

    def init_r(self):
        self.line_r.set_data([], [])
        return self.line_r,

    def animate_p(self,i):
        # get data from serial.
        ser_data = float(self.get_imu()[1])

        # this condition determines whether fill the canvas or scroll.
        if len(self.pitch_array) < X_LENGTH: # it just adds data until X_LENGTH of datas are accumulated.
            self.pitch_array = np.append(self.pitch_array, np.array([[len(self.pitch_array), ser_data]]), axis=0)
            # it adds data to yaw_array like this:
            # [[0,yaw(0)]]
            # [[0,yaw(0)], [1,yaw(1)]]
            # ...

            self.line_p.set_data(self.pitch_array[:, 0], self.pitch_array[:, 1])

        else:
            # if there are too much data to show, it would come here and strip the oldest data.
            # it works like this(this is the best way I can in limited time):
            # let X_LENGTH = 50,
            # [[0, yaw(0)] .....[49, yaw(49)]]
            # --(strip and add new data)--
            # [[1, yaw(1)] .....[50, yaw(50)]]
            # --(shift timeline)--
            # [[, yaw(1)] .....[49, yaw(50)]]

            new_data = np.append(self.pitch_array[1:, :], np.array([[len(self.pitch_array), ser_data]]), axis=0)
            subtract_arr = np.zeros((50, 2))  # create a new array to shift timeline.
            subtract_arr[:, 0] = 1
            new_data = new_data - subtract_arr
            self.pitch_array = new_data  # update new data to master data(yaw_array)

            self.line_p.set_data(new_data[:, 0], new_data[:, 1])

        return self.line_p,

    def animate_r(self, i):
        # get data from serial.
        ser_data = float(self.get_imu()[2])

        # this condition determines whether fill the canvas or scroll.
        if len(self.roll_array) < X_LENGTH: # it just adds data until X_LENGTH of datas are accumulated.
            self.roll_array = np.append(self.roll_array, np.array([[len(self.roll_array), ser_data]]), axis=0)
            # it adds data to yaw_array like this:
            # [[0,yaw(0)]]
            # [[0,yaw(0)], [1,yaw(1)]]
            # ...

            self.line_r.set_data(self.roll_array[:, 0], self.roll_array[:, 1])

        else:
            # if there're too much data to show, it would come here and strip the oldest data.
            # it works like this(this is the best way i can in limited time):
            # let X_LENGTH = 50,
            # [[0, yaw(0)] .....[49, yaw(49)]]
            # --(strip and add new data)--
            # [[1, yaw(1)] .....[50, yaw(50)]]
            # --(shift timeline)--
            # [[, yaw(1)] .....[49, yaw(50)]]

            new_data = np.append(self.roll_array[1:, :], np.array([[len(self.roll_array), ser_data]]), axis=0)
            subtract_arr = np.zeros((50, 2)) # create a new array to shift timeline.
            subtract_arr[:, 0] = 1
            new_data = new_data - subtract_arr
            self.roll_array = new_data # update new data to master data(yaw_array)

            self.line_r.set_data(new_data[:, 0], new_data[:, 1])
        return self.line_r,


    def animate_y(self,i):
        # get data from serial.
        ser_data = float(self.get_imu()[3])

        print(self.curr_data)

        # this condition determines whether fill the canvas or scroll.
        if len(self.yaw_array) < X_LENGTH: # it just adds data until X_LENGTH of datas are accumulated.
            self.yaw_array = np.append(self.yaw_array, np.array([[len(self.yaw_array), ser_data]]), axis=0)
            # it adds data to yaw_array like this:
            # [[0,yaw(0)]]
            # [[0,yaw(0)], [1,yaw(1)]]
            # ...

            self.line_y.set_data(self.yaw_array[:, 0], self.yaw_array[:, 1])

        else:
            # if there're too much data to show, it would come here and strip the oldest data.
            # it works like this(this is the best way i can in limited time):
            # let X_LENGTH = 50,
            # [[0, yaw(0)] .....[49, yaw(49)]]
            # --(strip and add new data)--
            # [[1, yaw(1)] .....[50, yaw(50)]]
            # --(shift timeline)--
            # [[, yaw(1)] .....[49, yaw(50)]]

            new_data = np.append(self.yaw_array[1:, :], np.array([[len(self.yaw_array), ser_data]]), axis=0)
            subtract_arr = np.zeros((50, 2)) # create a new array to shift timeline.
            subtract_arr[:, 0] = 1
            new_data = new_data - subtract_arr
            self.yaw_array = new_data # update new data to master data(yaw_array)

            self.line_y.set_data(new_data[:, 0], new_data[:, 1])
        return self.line_y,
    #
    # def anim_txt_p(self,i):
    #     self.p_txt.set_x(X_LENGTH)
    #     self.p_txt.set_y(float(self.read_serial()[1]))
    #     return self.p_txt,
    #
    # def anim_txt_r(self,i):
    #     self.r_txt.set_x(X_LENGTH)
    #     self.r_txt.set_y(float(self.read_serial()[2]))
    #     return self.r_txt,
    #
    # def anim_txt_y(self,i):
    #     self.y_txt.set_x(X_LENGTH)
    #     self.y_txt.set_y(float(self.read_serial()[3]))
    #     return self.y_txt,

    # def update_data(self,imu_data = np.array([])):

    def show_imu(self):

        anim_p = animation.FuncAnimation(self.fig, self.animate_p, init_func=self.init_p, frames=200, interval=INTERVAL, blit=False)
        anim_r = animation.FuncAnimation(self.fig, self.animate_r, init_func=self.init_r, frames=200, interval=INTERVAL, blit=False)
        anim_y = animation.FuncAnimation(self.fig, self.animate_y, init_func=self.init_y, frames=200, interval=INTERVAL, blit=False)

        # TBD : performance issue should be resolved.
        # anim_t = animation.FuncAnimation(self.fig, self.anim_txt_p, frames=200, interval=1, blit=False)
        # anim_t = animation.FuncAnimation(self.fig, self.anim_txt_r, frames=200, interval=1, blit=False)
        # anim_t = animation.FuncAnimation(self.fig, self.anim_txt_y, frames=200, interval=1, blit=False)

        plt.show()

    def capture_plot(self):
        return self.fig
