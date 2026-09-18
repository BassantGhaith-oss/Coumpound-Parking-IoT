import ssl
import time
import paho.mqtt.client as mqtt

HOST = ""
PORT = 8883

USER = ""
PASSWORD = ""

TOPIC = "Commpound Parking"

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(USER, PASSWORD)
mqtt_client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

mqtt_client.connect(HOST, PORT)

mqtt_client.loop_start()

print("Connected to MQTT broker...")

from gpiozero import Servo 
from time import sleep
from gpiozero import LED
from RPLCD.i2c import CharLCD
from gpiozero import Button
from gpiozero import DigitalInputDevice

lcd = CharLCD(
    'PCF8574',
    0x27,
    port=1,
    cols=16,
    rows=2
)

lcd.write_string("Smart Garage")

sw1 = DigitalInputDevice(5)
sw2 = DigitalInputDevice(6)
sw3 = DigitalInputDevice(13)
sw4 = DigitalInputDevice(19)

old_sw1 = 0
old_sw2 = 0
old_sw3 = 0
old_sw4 = 0

places = 0

button1 = Button(17)
button2 = Button(27)
button3 = Button(15)
button4 = Button(14)

p1=0
p2=0
p3=0
p4=0

servo = Servo(18)
led1 = LED(22)
led2 = LED(26)


while True:
    lcd.clear()
    if sw1.value == 1 and old_sw1 == 0:
       places += 1

    if sw2.value == 1 and old_sw2 == 0:
       places += 1

    if sw3.value == 1 and old_sw3 == 0:
       places += 1

    if sw4.value == 1 and old_sw4 == 0:
       places += 1

    if places == 0:
        led1.value=1
        led2.value=0
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Avaliable 4 parkings")

    elif places == 1:
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Avaliable 3 parkings")

    if places == 2:
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Avaliable 2 parkings")
        led2.value=1
        led1.value=0

    if places == 3:
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Avaliable 1 parkings")

    if places == 4:
        places= 0
        lcd.cursor_pos = (1, 0)
        lcd.write_string("No Parcking is Available")

    if button1.is_pressed:
        p1+=1
        if p1 ==1:
            servo.max()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Entering...")
            enter1=time.time()
            mqtt_client.publish(TOPIC, '{"spot":1,"status":"occupied"}')
            sleep(2)
            servo.min()
        if p1==2:
            p1=0
            servo.max()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Exiting...")
            exit1=time.time()
            sleep(2)
            total1 = exit1 - enter1
            money1 = total1 *0.005
            mqtt_client.publish(TOPIC, f'{{"spot":1,"status":"available","duration":{total1:.0f},"fee":{money1:.2f}}}')
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f"Time:{total1:.0f}s Fee:{money1:.2f}LE")
            servo.min()   
    if button2.is_pressed:
        p2+=1
        if p2 ==1:
            servo.max()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Entering...")
            enter2=time.time()
            mqtt_client.publish(TOPIC, '{"spot":2,"status":"occupied"}')
            sleep(2)
            servo.min()
        if p2==2:
            p2=0
            servo.max()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Exiting...")
            exit2=time.time()
            sleep(2)
            total2 = exit2 - enter2
            money2 = total2 *0.005
            mqtt_client.publish(TOPIC, f'{{"spot":2,"status":"available","duration":{total2:.0f},"fee":{money2:.2f}}}')
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f"Time:{total2:.0f}s Fee:{money2:.2f}LE")
            servo.min()   
    if button3.is_pressed:
        p3+=1
        if p3 ==1:
            servo.max()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Entering...")
            enter3=time.time()
            mqtt_client.publish(TOPIC, '{"spot":3,"status":"occupied"}')
            sleep(2)
            servo.min()
        if p3==2:
            p3=0
            servo.max()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Exiting...")
            exit3=time.time()
            sleep(2)
            total3 = exit3 - enter3
            money3 = total3 *0.005
            mqtt_client.publish(TOPIC, f'{{"spot":3,"status":"available","duration":{total3:.0f},"fee":{money3:.2f}}}')
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f"Time:{total3:.0f}s Fee:{money3:.2f}LE")
            servo.min()   
    if button4.is_pressed:
        p4+=1
        if p4 ==1:
            servo.max()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Entering...")
            enter4=time.time()
            mqtt_client.publish(TOPIC, '{"spot":4,"status":"occupied"}')
            sleep(2)
            servo.min()
        if p4==2:
            p4=0
            servo.max()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Exiting...")
            exit4=time.time()
            sleep(2)
            total4 = exit4 - enter4
            money4 = total4 *0.005
            mqtt_client.publish(TOPIC, f'{{"spot":4,"status":"available","duration":{total4:.0f},"fee":{money4:.2f}}}')
            lcd.cursor_pos = (0, 0)
