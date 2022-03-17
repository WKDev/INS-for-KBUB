## main.py
# fetches data from GPS and IMU
# Version 1.0.0 | First Creation
# Version 1.0.1 |
# Created : Chanhhyeok Son
# Date : Mar 13, 2022

from read_sensors import *
from typing import Optional
from fastapi import FastAPI

from realtime_plot import RTPlot

app = FastAPI()

if __name__ == '__main__':

    @app.get("/")
    def read_root():
        return {"Hello": "World"}


    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: Optional[str] = None):
        return {"item_id": item_id, "q": q}

    sensors = SensorReader(sensor_type='both')

    # it seems to need multiprocessing in order to visualize
    pt = RTPlot()

    pt.show_imu()

    # 센서 데이터를 어떻게 표시할 것인가 ?
    # fastapi 활용해서 현재 데이터를 구하기.
    # line , dot
    #
    # 1. flask 서버 열기
    # 2. 카카오맵 api

    #to run, run $uvicorn main:app --reload



    # while True:
    #     print(repr(sensors.read_gps()))
