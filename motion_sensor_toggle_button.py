from gpiozero import LED
from time import sleep
from gpiozero import MotionSensor
from gpiozero import Button
import requests

api_key = 'VRRIGRLCBLAHR6LV'
url = 'https://api.thingspeak.com/update'

green_led = LED(17)
pir = MotionSensor(4)
toggle_pin = 22
green_led.off()
counter = 0
toggle_button = Button(toggle_pin, pull_up=False, bounce_time=0.05)
is_active = False

def send_data(motion):
    response = requests.get(url,
        params = {
            'api_key': api_key,
            'field1': motion
        })
    print(response.json)


def toggle_def():
    global is_active
    print("Toggle Button Pressed")
    if is_active:
        is_active = False
    else:
        is_active = True

def main_loop():
    global counter, is_active
    while True:
        send_count = 0
        toggle_button.when_pressed = toggle_def
        if is_active:
            pir.wait_for_motion()
            send_count = 1
            print("Motion Detected")
            green_led.on()
            counter = counter + 1
            print(counter)
            pir.wait_for_no_motion()
            green_led.off()
            print("Motion Stopped")

        send_data(send_count)
        sleep(30)


if __name__ == '__main__':
    main_loop()
