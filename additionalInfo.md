# Reversing and exploiting the Passive Keyless Entry System over RF

## How Passive Keyless Entry works

Passive Keyless Entry (PKE) is the system that allows a user to enter their car without needing the user to physically interact with the key, either via using the physical key or pressing one of the buttons on the fob.  PKE works by having sensors around the car that look for both the user and the fob to be nearby.  In most cars this is simplified down to a capacitive sensor inside the door handle that alerts the car that someone is trying to enter it.  Once the car is alerted that an individual is trying to enter it, it begins a four way handshake to validate the fob and unlock the cars.  

| [Insert Image of car handle here] |
| :---: |
| As seen above, the inside of the car handle has two metal plates that act as a capacitive sensor.  Note there is also an antenna inside the handle that allows the car to hear the key fob wen it is talking at 315/434 MHz |

| [Insert Image of car handle capture here] |
| :---: |
| The handle transmits the output of the sensor down to the immobilizer system inside the car, when it see's that the sensor has been triggered, the immobilizer system has the car begin the four way handshake to unlock itself. |

The four way handshake can be broken into two sections, a static introduction and a dynamic passphrase.  For the first part of the handshake, the car begins the process by broadcasting a short static message on 134 kHz.  This message seems to be unique to each individual car manufacturer (Toyota, Ford, ect), and is used to ensure that a key fob from the same manufacturer is nearby.  When a fob from the same manufacturer is nearby, it replies with a short message on either 315MHz or 434MHz, depending on vendor and model.  Both of these messages are static, in that none of the bits change regardless of when or how often the message is sent.  