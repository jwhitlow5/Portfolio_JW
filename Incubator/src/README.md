# Custom-Built CO2 Incubator Project Overview

## Project Description
This project demonstrates the development of a custom-built CO2 incubator for studying the effects of electromagnetic fields on stem cell culture.  Designed for accurate temperature and CO2 level regulation, it's ideal for a range of biological and chemical experiments. 

## Key Features
- **Temperature and Humidity Control**: Utilizes an SHT31-based Grove temperature and humidity sensor for precise monitoring.
- **CO2 Regulation**: Features a high-accuracy NDIR CO2 sensor for meticulous CO2 level maintenance, with controlled gas release.
- **Automated Control**: The incubator's environment is managed through a Python script on the Raspberry Pi 4, ensuring precise and user-friendly operation.

## Example - GFP-positive Human Adipose Stem Cells (after 2 weeks of culture in incubator)
<img width="300" alt="image" src="https://github.com/jwhitlow5/jw_eng/assets/9408895/172dcbb8-927f-4be5-9a98-da202c6840d1">

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
- The Python script dynamically adjusts temperature and CO2 levels based on sensor readings, controlling the PTC heater and solenoid valve via IRF520 MOSFETs.

## Applications
- Suitable for cell culture in biological research and specialized chemical processes requiring controlled atmospheric and temperature conditions.

 