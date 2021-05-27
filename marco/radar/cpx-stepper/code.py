import board  # needed for everything
import neopixel  # needed for leds

import time  # needed for sleep
import busio  # needed for uart

from adafruit_crickit import crickit  # needed for crickit
from adafruit_motor import stepper  # needed for motor

# setup leds
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)
pixels.fill((0, 0, 255))

# min angle of stepper motor
stepAngle = 0.9

# setup uart
uart = busio.UART(board.TX, board.RX, baudrate=9600)

# handles rotating the stepper motor a specific angle and direction
def rotateMotor(direction, angle):
    count = round(float(angle) / stepAngle)

    if direction == 'F': # move forward
        for i in range(0, count, 1):
            crickit.stepper_motor.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        crickit.stepper_motor.release()
    else: # move backward
        for i in range(0, count, 1):
            crickit.stepper_motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        crickit.stepper_motor.release()

    response = "R " + direction + " " + str(count * stepAngle) + "\n"
    uart.write(response.encode())

# handles changing the color of the leds
def changeColor(r, g, b):
    pixels.fill((r, g, b))
    response = "C " + str(r) + " " + str(g) + " " + str(b) + "\n"
    uart.write(response.encode())

# main loop
while True:

    data = uart.read(32)  # read up to 32 bytes

    if data is not None:
        data_string = ''.join([chr(b) for b in data])

        if len(data_string) > 1:
            print(data_string)

            # split string into commands
            cmd = data_string.split()

            if cmd[0] == 'R' and len(cmd) >= 3:
                rotateMotor(cmd[1], cmd[2])
            elif cmd[0] == 'C' and len(cmd) >= 4:
                changeColor(int(cmd[1]), int(cmd[2]), int(cmd[3]))
            else:
                # transmit message back to alert of error
                msg = "ERROR 404 " + data_string + "\n"
                uart.write(msg.encode())

# Disconnected
print("DISCONNECTED")
