## DEPRECATED_Mar18, 2022

## data_fetcher.py
# fetches data from GPS and IMU
# Version 1.0.0 | First Creation
# Version 1.0.1 | Organized functions into one class
# Created : Chanhhyeok Son
# Date : Mar 14, 2022

from customthread import *
import pynmea2
# from vpython import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval

import threading

import time
t_start = time.time()


# box_object = box(visible=True)
# scene.width = 350
# scene.height = 300
# scene.range = 1.3
# scene.title = "Widgets (buttons, etc.)\n"
def anim(i, data):
    x = data['x']
    y = data['y']
    z = data['z']

    t = time.time()

    plt.cla()
    plt.subplot(311)
    plt.plot(t, x)

    plt.subplot(312)
    plt.plot(t, y)

    plt.subplot(313)
    plt.plot(t, z, 'r-')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.pause(0.05)


plt.style.use('fivethirtyeight')

#vars used for plot
x_vals = []
y_vals = []

x_q = Queue(maxsize=500)
t_q = Queue(maxsize=500)



def anim(i, x_data, y_data):
    x_vals.append(t_q.get())
    y_vals.append(x_q.get())

    plt.plot(x_vals,y_vals)

if __name__ == "__main__":
    fi = FetchINSData(mode='IMU', print_data=False)
    fi.init_serial()
    fi.init_thread()
    fi.start()







