# Marco Python script

import math # needed for hex to bin conversion

import yaml # needed for config file

import socket # needed for udp socket
import sys # needed for udp socket

from threading import Thread # needed for multithreading
import time # needed for sleep

from tkinter import Tk, filedialog as fd # needed for file dialog


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
    
    def __init__(self, txIP, txPN, txRPC, rxIP, rxPN, rxRPC):
        
        self.msgList = [] # the message list that will contain all the messages to transmit
        self.preBP = 0.0 # the previous bit period
        self.preRF = 0 # the previous response frequency
        
        # Creates the UDP sockets
        self.txSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rxSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Holds the server address for the TX source
        self.txAddress = (str(txIP), int(txPN))
        self.rxAddress = (str("0.0.0.0"), int(rxPN))
        
        #XMLRPC stuff : todo
        
    def sendMsg(self, message):
        """
        Generates and transmits the message

        Args:
            message (str): The PKE message in hex
        """

        #print(f'Sending: {str(message)}')

        self.txSocket.sendto(message.encode(), self.txAddress)
        
    def loadConfig(self):
        """
        Prompts the user for a config file to load into the message list
        """
        
        master = Tk()
        master.withdraw()
        
        keepAdding = 1
        
        while keepAdding:
            
            if len(self.msgList) < 1:
                fileName = fd.askopenfilename(parent=master, title='Select Config File', initialdir='.', filetypes=(('Yaml files', '*.yml'), ('All files', '*.*')))

                with open(fileName) as file:
                    documents = yaml.full_load(file)
                    
                    for item, doc in documents.items():
                        print(f"Loading: {str(item)}")
                        self.msgList.append(Message(doc))
                        print(f"\nMessage {str(len(self.msgList))}:")
                        self.msgList[len(self.msgList) - 1].printStats()
            else:
                keepAdding = input("Press 1 to add more config files, or anything else to continue: ")
                
                if keepAdding != '1':
                    break
                else:
                    fileName = fd.askopenfilename(parent=master, title='Select Config File', initialdir='.', filetypes=(('Yaml files', '*.yml'), ('All files', '*.*')))

                    with open(fileName) as file:
                        documents = yaml.full_load(file)
                        
                        for item, doc in documents.items():
                            print(f"Loading: {str(item)}")
                            self.msgList.append(Message(doc))
                            print(f"\nMessage {str(len(self.msgList))}:")
                            self.msgList[len(self.msgList) - 1].printStats()

    def runSchedule(self):
        """
        Runs the schedule for Marco
        """
        
        print("Starting Schedule process")
        
        while True:
            
            try:
                for i in range(len(self.msgList)):
                    #TODO: check pulse widths and freqs
                    
                    self.sendMsg(self.msgList[i].msg)
                    time.sleep(self.msgList[i].delay)
            except KeyboardInterrupt:
                print("Keyboard interrupt detected, closing program")
                break
            



if __name__ == "__main__":
    print("Starting Marco")
    
    schMan = ScheduleManager("127.0.0.1", "7331", "8008", "127.0.0.1", "7332", "8009") # creates the schedule manager
    
    schMan.loadConfig() # loads the config file
    
    schMan.runSchedule() # start transmitting