import serial # needed for serial

import random # used for testing
import time # used for testing

ser = serial.Serial('COM9', 9600)

while True:

    try:
        #time.sleep(10) # sleep just to make sure we don't overload

        if random.randint(0, 1) == 2: # color test - disabled
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            msg = "C" + " " + str(red) + " " + str(green) + " " + str(blue) 

            print("Transmitting: " + msg)
            ser.write(msg.encode())
            
            time.sleep(2.5)

        else: # motor test
            msg = ""
            angle = random.randint(0, 360)

            if random.randint(0, 1) == 1: # forward
                msg = "R F " + str(angle)
            else: # reverse
                msg = "R B " + str(angle)

            print("Transmitting: " + msg)
            ser.write(msg.encode())

            val = round(0.015 * angle) + 2

            time.sleep(val)

    except KeyboardInterrupt:
        print("Keyboard interrupt detected, ending program")
        break
