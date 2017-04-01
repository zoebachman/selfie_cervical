# device /dev/input/event3, name "Selfie-10", phys "b8:27:eb:69:a0:34"

import evdev
from time import sleep
from picamera import PiCamera


device = evdev.InputDevice('/dev/input/event3')

# camera code
camera = PiCamera()

camera.resolution = (1024, 768) #figure out what I want this to be
camera.start_preview()
#sleep(2)

count = 0

# reading the key press event and take a picture
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        while count < 3:
            #print event
            camera.capture('selfie' + str(count) + '.jpg' )
            count += 1
            print "took photo " + str(count)
        camera.close()
    

#gotta find a better way to close this


##    else:
##        print "no picture"
##        camera.close()





