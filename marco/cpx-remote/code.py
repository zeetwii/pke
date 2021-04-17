"""
Remote control code for the radar.  This code talks to the host over serial and then passes those commands via bluetooth to the other cpb.
Because somehow this doesn't work on the pi directly
"""

import board
import busio
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

uart = busio.UART(board.TX, board.RX, baudrate=9600)

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
        data = uart.read(32)  # read up to 32 bytes

        if data is not None:
            data_string = ''.join([chr(b) for b in data])

            if len(data_string) > 1:
                print(data_string)

                if send_packet(uart_connection, data_string):
                    if UARTService().in_waiting:
                        raw_bytes = UARTService().read(UARTService().in_waiting)
                        text = raw_bytes.decode().strip()
                        print("RX:", text)

                        uart.write(text.encode())
                else:
                    uart_connection = None
                    continue