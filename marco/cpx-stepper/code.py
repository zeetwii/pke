import board
import neopixel

import time
from adafruit_crickit import crickit
from adafruit_motor import stepper

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)

# min angle of stepper motor
stepAngle = 0.9

while True:
    print("WAITING...")
    pixels.fill((255, 255, 255))
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Connected
    ble.stop_advertising()
    print("CONNECTED")
    pixels.fill((0, 0, 255))

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

        response = "R " + direction + " " + str(count * stepAngle)
        uart_service.write(response.encode())

    # handles changing the color of the leds
    def changeColor(color):
        pixels.fill(color)
        response = "C " + str(color)
        uart_service.write(response.encode())

    # Loop and read packets
    last_send = time.monotonic()
    while ble.connected:
        # INCOMING (RX) check for incoming text
        if uart_service.in_waiting:
            raw_bytes = uart_service.read(uart_service.in_waiting)
            text = raw_bytes.decode().strip()
            #print("raw bytes =", raw_bytes)
            print("RX:", text)

            # split string into commands
            cmd = text.split()

            if cmd[0] == 'R' and len(cmd) >= 3:
                rotateMotor(cmd[1], cmd[2])
            elif cmd[0] == 'C' and len(cmd) >= 4:
                changeColor((int(cmd[1]), int(cmd[2]), int(cmd[3])))
            else:
                # transmit message back to alert of error
                msg = "ERROR 404 " + text
                uart_service.write(msg.encode())

    # Disconnected
    print("DISCONNECTED")

# Step motor in one direction forever
#while True:
    #crickit.stepper_motor.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    #time.sleep(0.001)  # minimum sleep between steps

    #for i in range(100):
        #crickit.stepper_motor.onestep(direction=stepper.FORWARD)

    #time.sleep(2)