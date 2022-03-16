## data_fetcher.py
# fetches data from GPS and IMU
# Version 1.0.0 | First Creation
# Version 1.0.1 | Organized functions into one class
# Created : Chanhhyeok Son
# Date : Mar 14, 2022

from customthread import *
import pynmea2

if __name__ == "__main__":
    fi = FetchINSData(mode='IMU', print_data=True)
    fi.init_serial()
    fi.init_thread()

    fi.start()


