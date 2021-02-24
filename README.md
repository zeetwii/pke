# Passive Keyless Entry Exploits

This repo contains gnuradio blocks and python scripts for emulating and spoofing the RF messages sent by the Passive Keyless Entry (PKE) system in a car to the key fob.  

All attacks in the repo are based on a 2014 Toyota Yaris, however the attack is easily customizable to other manufacturers.  

## What is this and Why do I care

The PKE system in the car is the one that handles functions like automatically unlocking your car door when your nearby or enabling the push to start functionality.  

As a part of how the PKE system operates, it has the ability to force the key fob to reply on demand.  This makes it ideal for active tracking and identification of a car over RF.  For a more detailed run down of everything, please look at this [additional information](./additionalInfo.md).

## Hardware needed

This attack has been performed using the following hardware:

- [HackRF SDR](https://greatscottgadgets.com/hackrf/one/)
- [Ham it Up upconverter](https://www.nooelec.com/store/sdr/sdr-addons/ham-it-up-plus.html)
- [YouLoop Antenna](https://airspy.com/youloop/)

This exact hardware setup is not needed.  Any SDR or SDR and upconverter which can transmit a signal on a 134 kHz center frequency will work.  The same is true for the antenna, you can carry out the attack using the same antenna your car uses if you don't mind grabbing it out of a junk lot.  

With that said, the advantage of the above components is that they are all fairly easy to assemble and set up.  So for any individual not familiar with the RF space, the above setup will be the easiest to work with, even if it does not provide the best performance.  

## Software needed

The only uncommon software needed for the pke code is [GNURadio](https://github.com/gnuradio/gnuradio).  The code that actually generates the PKE messages is a GNURadio OOT module, and thus requires a base version of GNURadio to be installed already.  Currently only GNUradio 3.8 is supported, however I am working on adding support for both 3.7 and 3.9.  To grab the OOT module, go to the gr folder that corresponds to your gnuradio version.

## Running the code

The attack is split into two programs, a [gnuradio flow graph](./gr-3.8/gr-pke/examples/pkeTransmit.grc) which generates the RF signal, and [messageGenerator](./messageGenerator.py) which handles creating the payload to transmit. 

Simply run both scripts and the attack should work.  Note that this is currently very much gradware, and the attack in auto mode of message generator is tied to the 2014 prius.  I'm working on expanding the script to make it easier to add and update what messages are automatically generated. 
