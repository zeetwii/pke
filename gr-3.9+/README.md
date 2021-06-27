# GR-PKE for GNURADIO 3.9

This code was written for gnuradio version 3.9

## Installation

To install it, follow the same steps for installing an OOT module in GNURadio.  For those not familiar with that process, that means make a build directory and then:

`cmake ..`

`make`

`sudo make install`

`sudo ldconfig`

Note, depending on where you installed gnuradio, you may need to add that path to the cmake command, for example:

`cmake -DCMAKE_INSTALL_PREFIX=/usr ..`

## Examples

Example flow graphs can be found in [examples](./gr-pke/examples/).  There are two main examples, decode and transmit.  

Transmit shows a working transmitter that was used to prove the attack, while decode shows a proof of concept decoder.  

For GR-3.10 : had to move xml files from /usr/share/gnuradio/grc/blocks/ to /usr/local/share/gnuradio/grc/blocks/
