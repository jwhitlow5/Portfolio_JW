import http.client
import urllib.parse

def publish_data(humidity, temperature, o2, co2, heating, solenoid, thingspeak_key, thingspeak_url):
    """
    Publishes sensor data to ThingSpeak.

    Parameters:
    - humidity (float): %relative humidity of chamber
    - temperature (float): avg chamber temperature
    - o2 (float): O2 concentration of chamber (ppm)
    - co2 (float): CO2 concentration of chamber (ppm)
    - heat_cycle (bool): status update
    - solenoid (bool): status update
    - thingspeak_key (str): The ThingSpeak API key.
    - thingspeak_url (str): The ThingSpeak URL.
    """
    params = urllib.parse.urlencode({'field1': humidity, 'field2': temperature, 
                                     'field3': co2, 'field4': o2, 
                                     'field5': heating, 'field6': solenoid, 
                                     'key': thingspeak_key}) 
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(thingspeak_url)
    published = False

    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        published = True
    except Exception as e:
        print("Error in publishing data:", e)

    return published
 