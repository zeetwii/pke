# Passive Keyless Entry RF Capture and Analysis Tutorial

This is a guide for how to capture and analyze the passive keyless entry messages of your own car.  To do so, you will need either a software defined radio (SDR) capable of recording on at least two channels at once, or two separate SDRs.  

## Introduction

So you want to capture and analyze your own PKE traffic?  Great, this guide is written to help you along and point out the key things you'll need to look for in order to perform a Marco attack on your own key fob.  

Before we get into how to capture and analyze PKE messages, a quick rundown of the hardware you'll need:

- An SDR capable of receiving on multiple channels, or two SDRs.
- An upconverter if your SDR is not capable of receiving 134 kHz signals.
- An antenna able to listen on 134 kHz.  
- An antenna able to listen on the frequency of your key fob.

Your car transmits its PKE messages at a very low frequency, 134 kHz.  This is a lower frequency than most commercial SDRs can detect on their own.  So you may need to use an upconverter to allow your SDR to capture the low frequency signal.  

You also may end up using two SDRs to capture the full PKE exchange.  This is because the two frequencies used by PKE are very far apart, and a single SDR cannot listen across the entire frequency range at once.  If you happen to have an SDR capable of receiving multiple channels at once, simply tune one channel to the cars frequency (134 kHz) and the other to your key fobs.  If you are using an SDR like a HackRF or an RTL-SDR, you will need to use two SDRs to capture both sides of the data link.  

You'll also need to figure out what frequency your key fob transmits on.  This varies for different makes and models of vehicles, and can be anywhere from 300 MHz to 900 MHz.  You can find out your key fobs frequency by looking up the FCC ID number printed on the key fob.  This will take you to the FCC record of your key fob, and will list what frequency it transmits on.  For most vehicles, this is somewhere between 315 MHz to 434 MHz.  

## Capturing the Signals

Once you have the hardware you need, and you've double checked what frequencies everything should transmit on, your ready to capture some signals.  Because PKE is a bidirectional data link, you will want to capture both sides of the data link at the same time.  This means the closer in time the two captures are to each other, the easier your analysis will be.  An example of how to do this is below:

| ![Insert image of pair capture](./photos/capTut/grPair.PNG) |
| :---: |
| This is the GNURadio flowgraph I used for all of my PKE captures.  In my case, I used two HackRF SDRs, with one connected to a Ham-It-Up Plus upconverter.  The upconverter shifts the 134 kHz transmissions from the car up to 125 MHz, allowing the HackRF to see and record them.  By starting both SDRs within the same flowgraph, I minimize the time offset I'll see when I analyze the two captures later.  There will still be a slight offset, because the HackRFs are started sequentially, but its very minor.  |

| ![Insert image of capture setup](./photos/capTut/capSetup.jpg) |
| :---: |
| This is hardware setup I used for my captures.  I placed both antennas in the passenger seat, with one antenna being a YouLoop small loop antenna, and the other is the ANT500 antenna that comes with the HackRF.  Each antenna is connected to a separate HackRF, and both SDRs are connected to my laptop.  |

## Signal Analysis

