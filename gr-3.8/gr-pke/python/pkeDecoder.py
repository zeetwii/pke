#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 zeetulsa.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy
from gnuradio import gr

class pkeDecoder(gr.sync_block):
    """
    docstring for block pkeDecoder
    """
    def __init__(self, ipAddr, portNum, multiplier):

        self.multi = int(multiplier)

        gr.sync_block.__init__(self,
            name="pkeDecoder",
            in_sig=[numpy.float32],
            out_sig=None)

    def toHex(self, message):
        '''
        Quick method to convert array to hex string
        '''
        binaryMsg = ''

        cutoffVal = self.multi / 2
        tempVal = 0

        for i in range(0, len(message), self.multi): # go through the bits of the message
            for j in range(self.multi): #cut out and compare chucks the length of multi
                
                if i + j >= len(message):
                    break
                else:
                    if message[i+j]: # if val is equalivant to a 1
                        tempVal = tempVal + 1 # increment tempVal

            if tempVal > cutoffVal:
                binaryMsg = binaryMsg + '1'
            else:
                binaryMsg = binaryMsg + '0'

            tempVal = 0 # reset tempVal

        '''
        for i in message:
            if i:
                binaryMsg = binaryMsg + '1'
            else:
                binaryMsg = binaryMsg + '0'
        '''

        hexStr = hex(int(binaryMsg, 2))
        print(hexStr)
        #print(f"Len: {str(len(binaryMsg))} : {binaryMsg}")



    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>

        msgSize = 24

        for i in range(len(in0)):
            if (i + (msgSize * self.multi)) < len(in0):
                if in0[i] and in0[i+1] and in0[i+2] and in0[i+3] and in0[i+4] and in0[i+5] and in0[i+6] and in0[i+7] and in0[i+8] and in0[i+9] and in0[i+10] and in0[i+11] and in0[i+12] and in0[i+13] and in0[i+14] and in0[i+15]:
                    self.toHex(in0[i:(i + (msgSize * self.multi))])
                    i = i + (msgSize * self.multi)
        

        return len(input_items[0])

