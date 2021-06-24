#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 ZeeTulsa.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import socket # needed for UDP

import numpy
from gnuradio import gr

class pkeGenerator(gr.sync_block):
    """
    docstring for block pkeGenerator
    """
    def __init__(self, ipAddr, portNum, multiplier):

        #multipler showing the ratio of sample rate to data rate
        self.mul = multiplier

        self.msgLeft = ''

        # create UDP socket
        self.recSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # bind socket
        self.recSocket.bind((str(ipAddr), int(portNum)))

        print(f"Binding Socket to: {str(ipAddr)} , {str(portNum)}")

        # set socket to nonblocking
        self.recSocket.setblocking(False)
        self.recSocket.settimeout(0)

        gr.sync_block.__init__(self,
            name="pkeGenerator",
            in_sig=None,
            out_sig=[numpy.float32])

    def decodeMsg(self, message):
        """
        Decodes the hex string into binary with all leading zeros

        Args:
            message (str): The hex string to decode
        """

        # Code to convert hex to binary 
        res = "{0:08b}".format(int(message, 16)) 

        corrected = ""

        for i in range(len(res)):
            corrected = corrected + (res[i] * self.mul)
        
        # Print the resultant string 
        #print ("Resultant transmission should be: ", str(corrected))

        return corrected 

    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        #out[:] = whatever

        # set everything to zero
        out[:] = numpy.float(0)

        # the value that will eventually hold the message
        msg = ''

        
        try:
            hexMsg = self.recSocket.recv(4096).decode()

            #print("Got message")

            # only update the message if we've finished sending the last one
            if not self.msgLeft:
                self.msgLeft = self.decodeMsg(hexMsg)
            else:
                print('Error, not finished transmitting previous msg')
        
        except socket.error:
            self.spacer = "0"
            #print("timeout")
        
        # if there is part of an old message left to tx, break it up and keep going
        if self.msgLeft:
            if(len(self.msgLeft) > len(out)):
                msg = self.msgLeft[0:len(out)]
                self.msgLeft = self.msgLeft[len(out):]
            else:
                msg = self.msgLeft
                self.msgLeft = ''
        else:
            msg = self.spacer

        for i in range(len(msg)):
            if msg[i] == '1':
                out[i] = numpy.float(1)
            else:
                out[i] = numpy.float(0)
        

        return len(output_items[0])

