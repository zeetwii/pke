# Marco Python script

import math # needed for hex to bin conversion

import yaml # needed for config file

import socket # needed for udp socket
import sys # needed for udp socket

from threading import Thread # needed for multithreading
import time # needed for sleep

from tkinter import filedialog as fd # needed for file dialog


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
        
        if len(doc) < 4:
            self.msg = "00000000"
            self.pulseWidth = 0.0002
            self.delay = 1
            self.responseFreq = 314350000
        else:
            self.msg = doc[0]
            self.pulseWidth = float(doc[1])
            self.delay = float(doc[2])
            self.responseFreq = int(doc[3])
            
            
    def printStats(self):
        """
        prints the settings of the message
        """
        
        print(f"Data: {self.msg}")
        print(f"Pulse Width: {str(self.pulseWidth)}")
        print(f"Replay Delay: {str(self.delay)}")
        print(f"Response Freq: {str(self.responseFreq)}")
        


class ScheduleManager:
    """
    Class that manages the scheduling for Marco
    """
    
    def __init__(self):
        
        self.msgList = [] # the message list that will contain all the messages to transmit
        self.preBP = 0.0 # the previous bit period
        self.preRF = 0 # the previous response frequency
        
    def loadConfig(self):
        """
        Prompts the user for a config file to load into the message list
        """
        
        fileName = fd.askopenfilename(title='Select Config File', initialdir='.', filetypes=(('Yaml files', '*.yml'), ('All files', '*.*')))

        with open(fileName) as file:
            documents = yaml.full_load(file)
            
            for item, doc in documents.items():
                print(f"Loading: {str(item)}")
                self.msgList.append(Message(doc))
                print(f"\nMessage {str(len(self.msgList))}:")
                self.msgList[len(self.msgList) - 1].printStats()




if __name__ == "__main__":
    print("Starting Marco")
    
    schMan = ScheduleManager() # creates the schedule manager
    
    schMan.loadConfig() # loads the config file