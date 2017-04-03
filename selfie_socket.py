# device /dev/input/event3, name "Selfie-10", phys "b8:27:eb:69:a0:34"
import io
import socket
import struct
import evdev
import time
from picamera import PiCamera


device = evdev.InputDevice('/dev/input/event3')


#Connect a client socket to my_server:8000 (change my_server to the hostname of your server)
client_socket = socket.socket()
#client_socket.connect(('my_server', 8000))
client_socket.connect(('128.122.6.170', 8000))

#Make a file-like object out of the connection
connection = client_socket.makefile('wb')

try:
    camera = PiCamera()

    camera.resolution = (1024, 768) #figure out what I want this to be
    camera.start_preview()
    sleep(2)

    count = 0

    #note the start time and construct a stream to hold image data
    #temporarily (we could write it directly to connection bu in this
    #case we want to find out the size of each capture first to keep
    #our protocol simple)
    start = time.time()
    stream = io.BytesIO()

    # reading the key press event and take a picture
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            while count < 3:
                #print event
                camera.capture('selfie' + str(count) + '.jpg' )
                count += 1
                print "took photo " + str(count)
            camera.close()

    for foo in camera.capture_continuous(stream, 'jpeg'):
        #Write the length of the capture to the stream and flush to
        #ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        #Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())
        #if we've been capturing for more than 30 seconds, quit
        if time.time() - start > 30:
            break
        #Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
    #Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
        
finally:
    connection.close()
    client_socket.close()
