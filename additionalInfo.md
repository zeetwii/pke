# Reversing and exploiting the Passive Keyless Entry System over RF

## How Passive Keyless Entry works

Passive Keyless Entry (PKE) is the system that allows a user to enter their car without needing the user to physically interact with the key, either via using the physical key or pressing one of the buttons on the fob.  PKE works by having sensors around the car that look for both the user and the fob to be nearby.  In most cars this is simplified down to a capacitive sensor inside the door handle that alerts the car that someone is trying to enter it.  Once the car is alerted that an individual is trying to enter it, it begins a four way handshake to validate the fob and unlock the cars.  

| ![Insert Image of car handle here](./photos/handleCables.jpg) |
| :---: |
| As seen above, the inside of the car handle has two metal plates that act as a capacitive sensor.  Note there is also an antenna inside the handle that allows the car to hear the key fob wen it is talking at 315/434 MHz |

| [Insert Image of car handle capture here] |
| :---: |
| The handle transmits the output of the sensor down to the immobilizer system inside the car, when it see's that the sensor has been triggered, the immobilizer system has the car begin the four way handshake to unlock itself. |

| [Insert diagram of the 4way handshake] |
| :---: |
| The diagram representing the four way handshake used to identify and validate the key fob by the car. |

The four way handshake can be broken into two sections, a static introduction and a dynamic passphrase.  For the first part of the handshake, the car begins the process by broadcasting a short static message on 134 kHz.  This message seems to be unique to each individual car manufacturer (Toyota, Ford, ect), and is used to ensure that a key fob from the same manufacturer is nearby.  When a fob from the same manufacturer is nearby, it replies with a short message on either 315MHz or 434MHz, depending on vendor and model.  Both of these messages are static, in that none of the bits change regardless of when or how often the message is sent.  

| [Insert Image of Initial Car message] |
| :---: |
| Above is the initial message that the car generates to see if any key fobs are nearby.  Note the message in the image is from a 2014 Toyota Prius, and will be different for other vendors |

| [Insert Image of Initial fob response] |
| :---: |
| The first message of the fob's response to the car, a static message that lets the car know that a fob is nearby.  Note this is the response from a 2014 Toyota Prius fob, and other vendors will have a different response in this field. |

The second part of the handshake is where we begin to see more unique and dynamic messages.  Where the first half of the handshake was to simply see if any relevant fob was nearby, this half focuses on uniquely identifying the fob, and issuing it a random challenge to solve.  This half starts with the car sending out a much longer message, that starts with the car's specific ID and ends with the seed the fob will use to solve it's challenge.  For the fob, it will first check to see if the car ID matches the one it has been paired with.  If the fob see's the car ID that it expects, it will then run the seed through it's proprietary algorithm and send that response, along with the fob's unique ID back to the car.  One key thing to note, it is only on the completion of this second half of the handshake that those fobs with an LED will light up and alert the user that they are transmitting.  

| [Insert Image of Second Car message] |
| :---: |
| Above is the message the car generates after it is alerted that there is possibly a valid fob nearby.  Note the message in the image is from a 2014 Toyota Prius, and will be different for other vendors |

| [Insert Image of Second fob response] |
| :---: |
| The second message the fob generates, this time responding to the challenge message from the car.  This message is only supposed to be generated if the fob and car have been paired.  Note this is the response from a 2014 Toyota Prius fob, and other vendors will have a different response in this field. |

## Using Passive Keyless Entry

Now that we have explained what PKE is, the question still exists: What can we do with it?  There are two basic uses for PKE from an attack perspective: more robust methods of key fob spoofing, and RF based identification and active tracking.

Most people are familiar with what is perhaps the most popular RF attack on cars, that of capturing and replaying a button press on the fob to the car.  While this tends to be more for show, due to only working once, there has been success on defeating the rolling code in the wild and spoofing the fob.  The attack tends to be complicated to carry out in the real world due to needing to record multiple button presses to being guessing where to start incrementing the rolling code.  By being able to decode and understand the PKE messages we reduce the number of captures needed to carry out this attack to one.  Once the attacker knows the unique ID of the key fob, everything else can be generated based on what the PKE system is asking for.  Note this path is mostly left for future work and is not the current focus of my research.  

The second, and in my opinion more novel, use of PKE is as a means to actively identify and track both cars and drivers via the key fob.  Currently most RF tracking systems for cars tend to focus on the Tire Pressure Monitoring System (TPMS), which works passively, generating messages every 30 seconds or so when traveling at speed.  Unlike TPMS, targeting the PKE system allows us to actively scan for and track targets.  An attacker can easily transmit multiple interrogations a second, allow for very rapid responses and high resolution tracking.  PKE also has the advantages of both listening to a more powerful transmitter, the fob in this case, and working even when the car is stopped or off.  

This dramatically changes the way vehicle tracking can work and what is possible in this space.  Rather than needing a complex camera system and neural network to identify and track cars real time, you instead just need a directional antenna that works at 134 kHz.  Because the key fob is relatively high powered compared to other transmitters in this space, a single SDR transmitting can easily cover a large parking lot with commercially available hardware.  

Given that the tracking focuses on the first half of the four way handshake, where the car is traditionally looking for a fob from the same manufacturer, we've decided to refer to this attack as Marco.  This is because the attack has a lot of similarities with game Marco Polo, both involve tracking and identifying multiple targets in a non-visual manner.  
