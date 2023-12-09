# Custom-Built CO2 Incubator Project Overview

## Project Description
I built a CO2-regulated stem cell culture incubator from scratch to facilitate a body of research on the effects of electromagnetic fields on stem cell growth. By developing a custom incubator, I was able to mount electromagnets and a brightfield microscope inside the incubator. I sourced the components individually and wrote the control loops regulating temperature, CO2, humidity, and O2 in Python. The code runs on a Raspberry Pi and uploads data to a cloud-based data logging platform for remote monitoring of incubator performance. [Source Code](https://github.com/jwhitlow5/Portfolio_JW/tree/master/Incubator/src/)

## Key Features
- **Temperature and Humidity Control**: Two SHT31 sensors are used to monitor temperature and humidity
- **CO2 Regulation**: An NDIR CO2 sensor measures the C02 concentration in ppm and the script controls a solenoid valve to regulate gas flow
- **Automated Control**: Data collection is done automatically and uploaded online from a Raspberry Pi 4. Additionally, electromagnets can be controlled with the Raspberry Pi, so the script can produce oscillating high frequency electromagnetic fields to influence cell growth.
  
## Usage in Research
[Remote-Controlled 3D Porous Magnetic Interface toward High-Throughput Dynamic 3D Cell Culture](https://pubs.acs.org/doi/abs/10.1021/acsbiomaterials.1c00459)

## Example - GFP-positive Human Adipose Stem Cells Grown and Imaged Inside Custom-Built Incubator
<img width="300" alt="image" src="https://github.com/jwhitlow5/Portfolio_JW/blob/master/Incubator/imgs/1.png">

## Materials List
1. **Raspberry Pi 4**:  [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
2. **CO2 Sensor (MH-Z16 NDIR)**:  [CO2 Sensor](https://sandboxelectronics.com/?product=100000ppm-mh-z16-ndir-co2-sensor-with-i2cuart-5v3-3v-interface-for-arduinoraspeberry-pi)
3. **Temperature and Humidity Sensor (SHT31)**:[SHT31 Sensor](https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-SHT31.html)
4. **Solenoid Valve for CO2 Control**: [12V Solenoid](https://www.mcmaster.com/products/solenoids/voltage~12v-dc/food-industry-solenoid-on-off-valves-9/)
5. **Heat element**: [12V PTC Heater](https://www.newegg.com/p/2C2-0085-01BP1)
6. **Adhesive Mount Heat Sink**: Dissipates heat efficiently. [Adhesive Heat Sink](https://www.mcmaster.com/products/heat-sinks/adhesive-mount-heat-sinks/)
7. **Electromagnets**: [12V Electromagnets](https://www.mcmaster.com/products/electromagnets/)
8. **IRF520 MOSFETs**: Switches for heavy loads like heaters and solenoids.

## Functionality
- The Python script dynamically adjusts temperature and CO2 levels based on sensor readings, controlling the PTC heater and solenoid valve via IRF520 MOSFETs. Data is uploaded to Thingspeak, a cloud-based logging service, so incubator conditions can be monitored remotely. Experiments with oscillating electromagnetic fields can be automated with Python scripts,


 
