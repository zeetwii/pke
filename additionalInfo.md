# Reversing and exploiting the Passive Keyless Entry System over RF

## How Passive Keyless Entry works

Passive Keyless Entry (PKE) is the system that allows a user to enter their car without needing the user to physically interact with the key, either via using the physical key or pressing one of the buttons on the fob.  PKE works by having sensors around the car that look for both the user and the fob to be nearby.  In most cars this is simplified down to a capacitive sensor inside the door handle that alerts the car that someone is trying to enter it.  Once the car is alerted that an individual is trying to enter it, it begins a four-way handshake to validate the fob and unlock the cars.  

| ![Insert Image of car handle here](./photos/handleCables.jpg) |
| :---: |
| As seen above, the inside of the car handle has two metal plates that act as a capacitive sensor.  To help protect the circuit, there was a weatherproof coating that had to be removed to access the pins.  Note there is also an antenna inside the handle that allows the car to hear the key fob wen it is talking at 315/434 MHz |

| ![Insert Image of car handle capture here](./photos/handleData.PNG) |
| :---: |
| The handle transmits the output of the sensor down to the immobilizer system inside the car, when it sees that the sensor has been triggered, the immobilizer system has the car begin the four-way handshake to unlock itself. In this image the middle row is the output of the capacitive sensor, and it goes low every time it is touched.  |

| ![Insert diagram of the 4way handshake](./photos/messageFlow.PNG) |
| :---: |
| The diagram representing the four-way handshake used to identify and validate the key fob by the car. |

The four-way handshake can be broken into two sections, a static introduction, and a dynamic passphrase.  For the first part of the handshake, the car begins the process by broadcasting a short static message on 134 kHz.  This message seems to be unique to each individual car manufacturer (Toyota, Ford, ect), and is used to ensure that a key fob from the same manufacturer is nearby.  When a fob from the same manufacturer is nearby, it replies with a short message on either 315MHz or 434MHz, depending on vendor and model.  Both messages are static, in that none of the bits change regardless of when or how often the message is sent.  

| ![Insert Image of Initial Car message](./photos/pkeInit.PNG) |
| :---: |
| Above is the initial message that the car generates to see if any key fobs are nearby.  Note the message in the image is from a 2014 Toyota Prius, and will be different for other vendors |

| ![Insert Image of Initial fob response](./photos/fobInitial.PNG) |
| :---: |
| The first message of the fob's response to the car, a static message that lets the car know that a fob is nearby.  Note this is the response from a 2014 Toyota Prius fob, and other vendors will have a different response in this field. |

The second part of the handshake is where we begin to see more unique and dynamic messages.  Where the first half of the handshake was to simply see if any relevant fob was nearby, this half focuses on uniquely identifying the fob, and issuing it a random challenge to solve.  This half starts with the car sending out a much longer message, that starts with the car's specific ID and ends with the seed the fob will use to solve its challenge.  For the fob, it will first check to see if the car ID matches the one it has been paired with.  If the fob see's the car ID that it expects, it will then run the seed through its proprietary algorithm and send that response, along with the fob's unique ID back to the car.  One key thing to note, it is only on the completion of this second half of the handshake that those fobs with an LED will light up and alert the user that they are transmitting.  

| ![Insert Image of Second Car message](./photos/pkeSecond.PNG) |
| :---: |
| Above is the message the car generates after it is alerted that there is a valid fob nearby.  Note the message in the image is from a 2014 Toyota Prius, and will be different for other vendors |

| ![Insert Image of Second fob response](./photos/fobSecond.PNG) |
| :---: |
| The second message the fob generates, this time responding to the challenge message from the car.  This message is only supposed to be generated if the fob and car have been paired.  Note this is the response from a 2014 Toyota Prius fob, and other vendors will have a different response in this field. |

## Using Passive Keyless Entry

Now that we have explained what PKE is, the question still exists: What can we do with it?  There are two basic uses for PKE from an attack perspective: more robust methods of key fob spoofing, and RF based identification and active tracking.

Most people are familiar with what is the most popular RF attack on cars, that of capturing and replaying a button press on the fob to the car.  While this tends to be more for show, due to only working once, there has been success on defeating the rolling code in the wild and spoofing the fob.  The attack tends to be complicated to carry out in the real world due to needing to record multiple button presses to being guessing where to start incrementing the rolling code.  By being able to decode and understand the PKE messages we reduce the number of captures needed to carry out this attack to one.  Once the attacker knows the unique ID of the key fob, everything else can be generated based on what the PKE system is asking for.  Note this path is mostly left for future work and is not the current focus of my research.  

The second, and more novel, use of PKE is to actively identify and track both cars and drivers via the key fob.  Currently most RF tracking systems for cars tend to focus on the Tire Pressure Monitoring System (TPMS), which works passively, generating messages every 30 seconds or so when traveling at speed.  Unlike TPMS, targeting the PKE system allows us to actively scan for and track targets.  An attacker can easily transmit multiple interrogations a second, allow for very rapid responses and high resolution tracking.  PKE also has the advantages of both listening to a more powerful transmitter, the fob in this case, and working even when the car is stopped or off.  

This dramatically changes the way vehicle tracking can work and what is possible in this space.  Rather than needing a complex camera system and neural network to identify and track cars real time, you instead just need a directional antenna that works at 134 kHz.  Because the key fob is high powered compared to other transmitters in this space, a single SDR transmitting can easily cover a large parking lot with commercially available hardware.  

Given that the tracking focuses on the first half of the four-way handshake, where the car is traditionally looking for a fob from the same manufacturer, we have decided to refer to this attack as Marco.  This is because the attack has a lot of similarities with game Marco Polo, both involve tracking and identifying multiple targets in a non-visual manner.  

## Marco

| ![Insert image of Marco setup](./photos/txSetup.jpg) |
| :---: |
| This is an example of the setup used to perform the Marco attack. Different antennas and SDRs can be used to adjust the size and range to the requirements of the attacker.  In the configuration shown, the total hardware cost to perform the attack is under $500.|

As discussed earlier, Marco is a new technique to allow for both active identification and tracking of cars and other PKE enabled vehicles over RF.  To perform this attack the attacker generates a series of PKE initialization messages, effectively mimicking a wide variety of different car manufactures at once.  The attacker than listens for the fob's initial response messages on 315 MHz and 434 MHz depending on the car manufacturer.  Because the attacker is the one generating the interrogation, they can control how many responses they get from the tracked vehicle and what the delay between interrogations is.  This allows much more flexibility than other passive methods like TPMS tracking.  Whereas TPMS only generates a message once every 30 seconds or so, Marco gives the attacker the option to interrogate multiple times a second.  This allows for much higher fidelity tracks than have normally been possible.  Additionally, while many people now carry around burner phones for discrete communications, few have dedicated themselves to having burner cars for transportation.  This means that once the attacker knows the car the target is using, they can easily track them across multiple days and weeks whenever the target is within range of the attacker.  

Below we'll discuss three implementations of Marco that focus on area surveillance, popup tracking, and known target validation.

### Area Surveillance

In this configuration, the attacker would be using omnidirectional antennas for both transmitting and receiving messages.  The attacker sends out a repeating string of PKE messages that mimic the initial PKE interrogation of a wide variety of different manufactures to cause any vehicle within range to respond.  Then the attacker can simply sit still and collect data.  

This technique has an advantage over current surveillance methods because the attacker can cover a large area with only a single deployed asset.  Additionally, the observer system can be out of line of sight of the area it is scanning, allowing the system to be farm more discrete than current monitoring systems.  

### Popup Tracking

If either the transmit or receive setup is using a directional antenna, the attacker can find the relative position of the car to themselves by figuring out the angle of arrival of the signal, and then using the change in signal strength to decide if the car is traveling towards or away from them.  Then, assuming the attacker is also able to move positions at a speed faster than the vehicle being tracked, the attacker can begin closing in on the target until it is within visual range.  

In theory the attacker can freely switch between this mode and area surveillance at any point in time.  This gives the attacker the advantage of staying out of sight only until a suspected target of interest enters their space.  

### Target Validation

The above uses of Marco focus on exploiting the first half of the four-way handshake, because those exploits require zero previous knowledge of the vehicle being tracked.  However, each of those techniques can only tell the attacker that a vehicle from a given manufacturer of a specific type is nearby.  But what if the attacker wants to only target a single specific vehicle and ignore all others?  If the attacker has been able to capture a single instance of a full four-way PKE handshake from their target, this can be done.  

Recall that the first half of the PKE handshake is static, while the second half is dynamic.  The dynamic section involves both the car and fob transmitting their unique ID to validate each other.  If the attacker knows the unique ID of the fob they are tracking, they can use that to specifically track and validate that they are targeting that fob and that fob alone.  

The reason for this is that while the two validating messages are dynamic, they are also repeatable.  The car transmits its car ID and a seed that acts as the question, while the fob responds with its own ID and the solution it's calculated using the provided seed.  The key thing to know is that the fob will give the exact same answer every time it is presented with that seed.  This means that once the attacker can record the car ID that the fob has been paired to, they can either replay the capture message or simply pass in a dummy seed value and listen for the fob's response.  The advantage of all this extra work is that now they can look and track for a single specific fob ID, or validate over RF that the vehicle they are tracking is the one that they think it is.  
