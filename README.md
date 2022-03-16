# Localization GPS+IMU Comm. Demo
## Introduction
It is INS System for Autonomous Car.

## Why We Call it INS?
 - Basically, INS is for letting car know where am I. It seems to be enough to find the location without GPS. But Actually, It is not. GPS is affected by a lot of factors(weather, circumstance(In worst case, GPS may not get data if the environment surrouned by building,), electromagnetic...). These makes a lot of noise. It makes unstable movement of Autonomous Car. So We need to improve the stability and sustainabilty of Localization. 
 - In Localization, We use GPS and IMU together. that's what we call 'INS'

## How It works?
 In order to improve the performance of Localization, It stablizes the sensor data executing below tasks:
 1. Using UKF to improve the precision of GPS data.
 2. Measuring Moving distance using IMU.
 3. Incorporate two datas(ususally we call it 'Sensor Fusion')
 4. Returns accurate localization data.

 ## Input and Output Summary
 ### Input(Input's are connected by Serial.)
  - GPS | NMEA Data
 - IMU | (X,Y,Z) Euler Angle(We don't deal with Data correction from imu.)

### Output
 - Localization Data(lat, lon, heading)



## Hardware
GPS | Ublox C94-M8P-2 (It supports any GPS in case your GPS qualifies NMEA protocol.)
IMU | E2BOX AHRS EBIMU-9DOFV5

## Changelog
* v1.0.0  | Mar 14, 2022 Created





