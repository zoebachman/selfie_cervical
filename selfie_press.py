# device /dev/input/event3, name "Selfie-10", phys "b8:27:eb:69:a0:34"

import evdev
from time import sleep
from picamera import PiCamera


device = evdev.InputDevice('/dev/input/event3')

# camera code

camera = PiCamera()

camera.resolution = (1024, 768)
camera.start_preview()
sleep(2)

# reading the key press event and take a picture
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        print(categorize(event))
        camera.capture('selfie.jpg')





