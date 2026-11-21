# dht mittarin testaus

#tuodaan tarvittavat kirjastot
import dht
import machine
import time
import network
from umqtt.simple import MQTTClient

SSID = "raimos26"
PASSWORD = "22061996"

#yhdistetään nettiin
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Yhdistetään verkkoon…")
while not wlan.isconnected():
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("IP-osoite:", ip)

#yhdistetään mqqt brokeriin
client = MQTTClient(
b"picow",
"iot.research.hamk.fi")






#sensori muuttuja
sensor = dht.DHT22(machine.Pin(21))


#mitataan lämpötilaa ja kosteutta 10 sekunnin välein
while True:
    #eka mittaus
    sensor.measure()
    kosteus = sensor.humidity()
    lampotila = sensor.temperature()
    #toinen mittaus
    sensor.measure()
    uusikosteus = sensor.humidity()
    uusilampotila = sensor.temperature()


    if uusikosteus != kosteus:
        
        print("kosteus",kosteus,"%","lähetetty mqqt")
        #lähetetään mqqt viesti
        client.connect()
        client.publish(
            b"HAMK/Fo/DHT22/2604987/kosteus",
            b"kosteus muuttui"
            )
        client.disconnect()

    if uusilampotila != lampotila:
        print("lämpötila",lampotila,"celsiusta","lähetetty mqqt")
        #lähetetään mqqt viesti
        client.connect()
        client.publish(
            b"HAMK/Fo/DHT22/2604987/lampotila",
            b"lampotila muuttui"
            )
        client.disconnect()

    else:
        print("lämpötila: ",lampotila,",""celsiusta","kosteus: ",kosteus,"%")
    #toistetaan 10 sekunnin välein mittaus
    time.sleep(10)