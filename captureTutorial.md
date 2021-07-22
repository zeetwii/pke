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

To actually capture the signals, I start my gnuradio script and then press the push to start button of the car several times.  This turns the car on and off, and lets me get several versions of the messages being exchanged.  You can get the same traffic by opening and closing the door from outside the car, but I find its easier to just sit in the vehicle and not move around.  

## Signal Analysis

Now that we have the captures from both the car and the key fob, its time to analyze them to see how the data link works.  To do that, I personally use a tool called [Inspectrum](https://github.com/miek/inspectrum).  Inspectrum allows you to visualize the complex file you just recorded and analyze the data within the signals.  It's not the only tool that can do this, so feel free to use another if you have your own preferences.  

| ![Insert image of inspectrum](./photos/capTut/analysis.PNG) |
| :---: |
| This is what the two captures I recorded look like when opened with inspectrum.  Imb.cfile contains the PKE messages that the car is transmitting at 134 kHz, while fob.cfile contains the message the key fob is transmitting at 315 MHz.  |

Above is a screen shot of what the captures I took look like in inspectrum.  Because I started both SDRs at the same time, the run time of each file is the same, allowing me to match the signals.  In the photo, you can see that the car begins transmitting two messages around 6.6 seconds into the capture.  The key fob responds at the same time, with the pattern being a short message from the car, a short message from the fob, a long message from the car, and finally a long message from the fob.  These four messages make up the four-way handshake.  In your case, you should see either two or four messages here.  If you see four messages, like in the image above, congratulations: your vehicle uses the traditional version of the four-way handshake, with wake-up, acknowledgement, challenge and response messages.  If you only see two messages, that means your vehicle uses the alternative form of the four-way handshake.  This form consists of only the challenge and response messages.  While this means that attacks targeting the wake-up message won't affect your key fob, you can still attack it using the challenge message.  

### Collecting the data needed for Marco

Now that we have the captures, and we've confirmed what implementation of the four-way handshake the vehicle is using, its time to collect the data needed to carry out a Marco attack.  To do that, we need to measure two things using the cars capture file: the bit period, and the message data.  The bit period is the length of time that it takes to transmit a single bit.  Its related to the data rate of the message, but unlike the message rate, the bit period is pretty easy to measure.  Below is an example of how to measure the bit period:

| ![Insert image of bp](./photos/capTut/bp.PNG) |
| :---: |
| To find the bit period, use the cursor to select what looks to be a single bit of data from the message.  In the photo above, I've zoomed in on inspectrum to get a better view and I highlighted and measured what is a single bit in the wake-up message.  |

Getting the exact value can be a little challenging, and you may have to adjust your power settings to make sure the signal isn't getting washed out.  Once you have the bit period, its easy to solve for the message data.  All of the messages transmited by the car are in a format known as Amplitude Modulated On-Off Keying (AMOOK).  This means that a digital one is represented by the signal being present, and a digital zero is represented by it being absent.  

Now would also be a good time to mention that there is a slight distortion in the capture I've been showing.  Because the SDR was capturing a signal so close to what is effectively 0 Hz for the upconverter, the signals near that edge were mirrored.  This is why the same signal shows up at both +134 kHz and -134 kHz.  They're not two different signals, they're the same one mirrored by the SDR as its trying to process data from the upconverter along a weird edge case.  

Once you have both your bit period and message data, your ready to program and launch your attack.  