"""
Remote control code for the radar.  This code talks to the host over serial and then passes those commands via bluetooth to the other cpb.
Because somehow this doesn't work on the pi directly
"""

import board
#import neopixel

import time
from adafruit_circuitplayground.bluefruit import cpb

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

def send_packet(uart_connection_name, msg):
    """Returns False if no longer connected."""
    try:
        uart_connection_name[UARTService].write(msg.encode())
    except:  # pylint: disable=bare-except
        try:
            uart_connection_name.disconnect()
        except:  # pylint: disable=bare-except
            pass
        return False
    return True


ble = BLERadio()
#pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)
cpb.pixels.brightness = 0.1

# Setup for preventing repeated button presses and tracking switch state
button_a_pressed = False
button_b_pressed = False

uart_connection = None
# See if any existing connections are providing UARTService.
if ble.connected:
    for connection in ble.connections:
        if UARTService in connection:
            uart_connection = connection
        break

while True:
    if not uart_connection or not uart_connection.connected:  # If not connected...
        print("Scanning...")
        cpb.pixels.fill((255, 255, 255))
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):  # Scan...
            if UARTService in adv.services:  # If UARTService found...
                print("Found a UARTService advertisement.")
                cpb.pixels.fill((0, 0, 255))
                uart_connection = ble.connect(adv)  # Create a UART connection...
                break
        # Stop scanning whether or not we are connected.
        ble.stop_scan()  # And stop scanning.
    while uart_connection and uart_connection.connected:  # If connected...
        if cpb.button_a and not button_a_pressed:  # If button A pressed...
            print("Button A pressed.")
            # Send a LEFT button packet.
            if not send_packet(uart_connection,"R F 90"):
                uart_connection = None
                continue
            button_a_pressed = True  # Set to True.
            time.sleep(0.05)  # Debounce.
        if not cpb.button_a and button_a_pressed:  # On button release...
            button_a_pressed = False  # Set to False.
            time.sleep(0.05)  # Debounce.
        if cpb.button_b and not button_b_pressed:  # If button B pressed...
            print("Button B pressed.")
            # Send a RIGHT button packet.
            if not send_packet(uart_connection, "R B 90"):
                uart_connection = None
                continue
            button_b_pressed = True  # Set to True.
            time.sleep(0.05)  # Debounce.
        if not cpb.button_b and button_b_pressed:  # On button release...
            button_b_pressed = False  # Set to False.
            time.sleep(0.05)  # Debounce.
        time.sleep(0.1)  # Delay to prevent sending packets too quickly.