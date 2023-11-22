import grovepi #i2c sensor bridge
import sys
import time
from grove.i2c import Bus
import serial
from data_publisher import publish_data  

# Function for CRC calculation
def calculate_crc(data):
    crc = 0xff
    for s in data:
        crc ^= s
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x131
            else:
                crc <<= 1
    return crc

class GroveTemperatureHumiditySensorSHT3x(object):
    def __init__(self, address=0x44, bus=None):
        self.address = address
        self.bus = Bus(bus) 

    def read(self):
        self.bus.write_i2c_block_data(self.address, 0x24, [0x00])
        time.sleep(0.016) 

        data = self.bus.read_i2c_block_data(self.address, 0x00, 6)

        if data[2] != calculate_crc(data[:2]):
            raise ValueError("Temperature CRC mismatch")
        if data[5] != calculate_crc(data[3:5]):
            raise ValueError("Humidity CRC mismatch")

        temperature = (data[0] << 8) + data[1]
        celsius = -45 + (175 * temperature / 65535.0)
        humidity = 100 * ((data[3] << 8) + data[4]) / 65535.0

        return celsius, humidity

def read_o2_voltage(pin, vref):
    sum_voltages = 0
    readings_count = 5

    for _ in range(readings_count):
        sum_voltages += grovepi.analogRead(pin)

    average_voltage = sum_voltages / readings_count
    measured_voltage = average_voltage * vref / 1023

    return measured_voltage

def read_o2_concentration(pin, vref):
    measured_voltage = read_o2_voltage(pin, vref)
    o2_concentration = measured_voltage * 0.21 / 2.0
    return o2_concentration * 100

def read_co2_concentration(serial_connection):
    ppm_co2 = 0

    if serial_connection.in_waiting > 0:
        serial_connection.flushInput()
        time.sleep(1)

        for i in range(1, 3):
            serial_connection.flushInput()
            serial_connection.write(bytes(b'\xFE\x44\x00\x08\x02\x9F\x25'))
            time.sleep(0.5)
            response = serial_connection.read(7)
            high = int(response[3])
            low = int(response[4])
            co2 = (high * 256) + low
            co2 *= 10

            if i > 1:
                ppm_co2 = (ppm_co2 + float(co2)) * 0.5
            else:
                ppm_co2 = float(co2)
            print(str(ppm_co2))
            time.sleep(0.1)

    return ppm_co2

def main():
    #init
    global THINGSPEAKKEY
    THINGSPEAKKEY = ""
    global THINGSPEAKURL
    heatRelay = 2 #digital pin on ras pi 4 for heater mosfet
    solRelay = 3 #digital pin on ras pi 4 for solenoid mosfet
    tempSet=37 #set temperature Celcius
    tTol=1 #set temperature tolerance
    co2Set=50000 #set ppm CO2
    cTol=2000 #tolerance ppm CO2
    heating=False
    solenoid=False
    ser = serial.Serial('/dev/serial0', 9600) #serial comms, baud rate 9600
    THINGSPEAKURL="api.thingspeak.com:80"
    analog_pin = 1 # refers to A0 port
    vref = 5.0 # ADC voltage reference
    sensor1 = GroveTemperatureHumiditySensorSHT3x(0x43) #i2c address of sensor 1
    sensor2 = GroveTemperatureHumiditySensorSHT3x(0x45) #i2c address of sensor 2
    grovepi.pinMode(heatRelay,"OUTPUT")
    grovepi.digitalWrite(heatRelay,0)
    grovepi.pinMode(solRelay, "OUTPUT")
    grovepi.digitalWrite(solRelay,0)


    while True:
        temperature1, humidity1 = sensor1.read()
        temperature2, humidity2 = sensor2.read()
        temp = 0.5*(float(temperature1)+float(temperature2))
        rh = 0.5*(float(humidity1)+float(humidity2))    
        o2_conc = read_o2_concentration(analog_pin, vref)  
        co2_conc = read_co2_concentration(ser)  
        print('[O2 concentration = {:5.2f}],[CO2 ppm = {:5.2f}],[Avg T = {:5.2f}],[Avg humidity = {:5.2f}]'.format(o2_conc,co2_conc,temp,rh))
        
        if temp>tempSet:
            
            grovepi.digitalWrite(heatRelay,0)
            heatTime=False
        else:
            if abs(temp-tempSet)>tTol:
                grovepi.digitalWrite(heatRelay,1)
                heatTime=True

        if co2_conc>co2Set:
            grovepi.digitalWrite(solRelay,0)
            solTime=False
        else:
            if abs(co2_conc-co2Set)>cTol:
                grovepi.digitalWrite(solRelay,1)
                soltime=True
        try:
            published=publish_data(rh, temp, o2_conc, co2_conc,heating,solenoid)
        except:
            print("err")
        if published==False:
            print("error publishing")
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('[Keyboard interrupted]')
        grovepi.digitalWrite(2,0)
        grovepi.digitalWrite(3,0)
        
        sys.exit(0)
    except IOError:
        print('[IO Error]')
        grovepi.digitalWrite(3,0)
        grovepi.digitalWrite(2,0)
        
        sys.exit(0)
    except ValueError as e:
        print('[{}]'.format(str(e)))
        sys.exit(0)