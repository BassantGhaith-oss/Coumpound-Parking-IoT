import ssl
import time
import paho.mqtt.client as mqtt

HOST = "0caac27879564822a33b169380449b6e.s1.eu.hivemq.cloud"
PORT = 8883

USER = "deleted later"
PASSWORD = "deleted later"

TOPIC = "Commpound Parking"

mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.username_pw_set(USER, PASSWORD)
mqtt_client.tls_set(cert_reqs=ssl.CERT_REQUIRED)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker...")
    else:
        print(f"MQTT connect failed, rc={rc}")


def on_disconnect(client, userdata, rc):
    print(f"MQTT disconnected, rc={rc}")


mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect

try:
    mqtt_client.connect(HOST, PORT)
    mqtt_client.loop_start()
except Exception as e:

    print(f"Could not connect to MQTT broker: {e}")

from gpiozero import Servo
from gpiozero import LED
from gpiozero import Button
from gpiozero import DigitalInputDevice
from RPLCD.i2c import CharLCD

lcd = CharLCD(
    'PCF8574',
    0x27,
    port=1,
    cols=16,
    rows=2
)

lcd.clear()
lcd.write_string("Smart Garage")


sw1 = DigitalInputDevice(5, pull_up=True)
sw2 = DigitalInputDevice(6, pull_up=True)
sw3 = DigitalInputDevice(13, pull_up=True)
sw4 = DigitalInputDevice(19, pull_up=True)

button1 = Button(17, pull_up=True, bounce_time=0.2)
button2 = Button(27, pull_up=True, bounce_time=0.2)
button3 = Button(15, pull_up=True, bounce_time=0.2)
button4 = Button(14, pull_up=True, bounce_time=0.2)

servo = Servo(18)
led1 = LED(22)
led2 = LED(26)


servo.min()


old_places = -1 


spot_state = {1: "idle", 2: "idle", 3: "idle", 4: "idle"}
spot_action_until = {1: 0, 2: 0, 3: 0, 4: 0}
spot_enter_time = {1: None, 2: None, 3: None, 4: None}
ACTION_DURATION = 2  

buttons = {1: button1, 2: button2, 3: button3, 4: button4}
old_button_pressed = {1: False, 2: False, 3: False, 4: False}


def start_entering(spot):
    servo.max()
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Entering...")
    spot_enter_time[spot] = time.time()
    mqtt_client.publish(TOPIC, f'{{"spot":{spot},"status":"occupied"}}')
    spot_state[spot] = "entering"
    spot_action_until[spot] = time.time() + ACTION_DURATION


def start_exiting(spot):
    servo.max()
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Exiting...")
    spot_state[spot] = "exiting"
    spot_action_until[spot] = time.time() + ACTION_DURATION


def finish_action(spot):
    servo.min()
    if spot_state[spot] == "entering":
        spot_state[spot] = "occupied"
    elif spot_state[spot] == "exiting":
        total = time.time() - spot_enter_time[spot] if spot_enter_time[spot] else 0
        fee = total * 0.005
        mqtt_client.publish(
            TOPIC,
            f'{{"spot":{spot},"status":"available","duration":{total:.0f},"fee":{fee:.2f}}}'
        )
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(f"Parking {spot}")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"Fee:{fee:.2f}LE")
        spot_state[spot] = "idle"


while True:

    now = time.time()

   
    places = sum(1 for sw in (sw1, sw2, sw3, sw4) if sw.value == 0)

  
    for spot, btn in buttons.items():
        pressed = btn.is_pressed
        if pressed and not old_button_pressed[spot]:
            if spot_state[spot] == "idle":
                start_entering(spot)
            elif spot_state[spot] == "occupied":
                start_exiting(spot)
         
        old_button_pressed[spot] = pressed

   
    for spot in (1, 2, 3, 4):
        if spot_state[spot] in ("entering", "exiting") and now >= spot_action_until[spot]:
            finish_action(spot)

    
    any_spot_busy = any(s in ("entering", "exiting") for s in spot_state.values())

    if not any_spot_busy and places != old_places:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Smart Garage")
        lcd.cursor_pos = (1, 0)

        if places == 0:
            led1.value, led2.value = 1, 0
            lcd.write_string("4 parkings")
        elif places == 1:
            led1.value, led2.value = 1, 0
            lcd.write_string("3 parkings")
        elif places == 2:
            led1.value, led2.value = 0, 1
            lcd.write_string("2 parkings")
        elif places == 3:
            led1.value, led2.value = 0, 1
            lcd.write_string("1 parking")
        else:  # places == 4
            led1.value, led2.value = 0, 1
            lcd.write_string("No Parking")

        old_places = places

    time.sleep(0.1)
