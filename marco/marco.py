# Marco Python script

import math # needed for hex to bin conversion

import yaml # needed for config file

import socket # needed for udp socket
import sys # needed for udp socket

from threading import Thread # needed for multithreading
import time # needed for sleep


class Message:
    """
    Class that represents each message Marco will transmit
    """
    
    def __init__(self, doc):
        """
        Initializes the message

        Args:
            doc (String Array): Array of at least 5 elements pulled from config file
        """
        
        if len(doc) < 5:
            self.msg = "00000000"
            self.centerFreq = 134000
            self.pulseWidth = 0.0002
            self.repeat = 0
            self.repeatSpace = '0' * len(self.msg)
            self.delay = 1
        else:
            self.msg = doc[0]
            self.centerFreq = int(doc[1])
            self.pulseWidth = float(doc[2])
            self.repeat = int(doc[3])
            self.repeatSpace = '0' * len(self.msg)
            self.delay = int(doc[4])
            
            
    def printStats(self):
        """
        prints the settings of the message
        """
        
        print(f"Data: {self.msg}")
        print(f"Center Freq: {str(self.centerFreq)}")
        print(f"Pulse Width: {str(self.pulseWidth)}")
        print(f"Repeat Amount: {str(self.repeat)}")
        print(f"Repeat Space: {str(self.repeatSpace)}")
        print(f"Replay Delay: {str(self.delay)}")
        







if __name__ == "__main__":
    print("Starting Marco")
    
    # the message list that will contain all the messages to transmit
    msgList = []
    
    fileName = input("\nEnter config file to use: ")
    
    with open(fileName) as file:
        documents = yaml.full_load(file)
        
        for item, doc in documents.items():
            msgList.append(Message(doc))
            print(f"\nMessage {str(len(msgList))}:")
            msgList[len(msgList) - 1].printStats()