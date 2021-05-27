# Installing GNURadio and RFRE tools on a VM

## VM Setup

- Use latest version of Ubuntu LTS when possible
- Give VM as much ram and CPU cores as you can spare
  - GNURadio is very memory and CPU intensive for a lot of the operations we use it for
- Make sure your USB driver is set to USB 3.0

## UHD setup

In order to have proper compatibility with GNURadio, you need to install UHD before you install GNURadio or else you will get weird behaviors whenever you use an Ettus SDR

Note, instructions taken from UHD installation page: <https://files.ettus.com/manual/page_install.html>

Ettus has moved to providing Ubuntu packages through a Personal Package Archive (PPA). This enables automatic updates and better integration with Ubuntu's package manager, APT.

<https://launchpad.net/~ettusresearch/+archive/ubuntu/uhd>

After adding the PPA to ubuntu and running `sudo apt update`, install the following utilities:

`sudo apt-get install libuhd-dev libuhd3XXX uhd-host`

Note: the actual number after libuhd will change often.  Just use whatever one is there.

## GNURadio

Note: instructions taken from [installingGR](https://wiki.gnuradio.org/index.php/InstallingGR) and [UbuntuInstall](https://wiki.gnuradio.org/index.php/UbuntuInstall#Install_Dependencies)

For Ubuntu 20.04 and up: 

```bash

sudo apt install git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy 
python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev 
libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 
liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins 
python3-zmq python3-scipy python3-gi python3-gi-cairo gir1.2-gtk-3.0 libcodec2-dev  libgsm1-dev pybind11-dev python3-matplotlib libsndfile1-dev

```

Additionally, you will want to go ahead and install the drivers for Hackrf, rtl-sdr, and any other sdrs you plan to use right now.  

For example, with hackrf, that means running `sudo apt install hackrf libhackrf-dev`

Step 1: Installing Dependencies

Refer to this page for your specific Linux distro to find how to install dependencies. For example, on Ubuntu 20.04 use this command.
Step 2: Installing Volk

- cd
- git clone --recursive <https://github.com/gnuradio/volk.git>
- cd volk
- mkdir build
- cd build
- cmake -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python3 ../
- make
- make test
- sudo make install

If you're running Linux, then always remember to do the following command after installing any library:

- sudo ldconfig

Step 3: Installing GNU Radio

- cd 
- git clone <https://github.com/gnuradio/gnuradio.git>
- cd gnuradio

Note: If you want to build the maint-3.9 branch rather than the default master branch, enter: git checkout maint-3.9 and then

- mkdir build
- cd build

Note: In the following command, you can add -DCMAKE_INSTALL_PREFIX=XXX to install GNU Radio into the PREFIX XXX; if not specified, then the PREFIX is /usr/local. See other CMake options in Common cmake flags.

- cmake -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python3 ../
- make -j3 (e.g. if you want to use 3 CPU cores during the build. To use 8 do -j8, to use 1 leave out the -j flag.)

Note: In the following command, it is very possible that not all tests pass. Generally any error is a sign of a missing dependency such as the Python interface to ZMQ or NumPy or SciPy, none of which are required for building GNU Radio but are required for testing.

- make test
- sudo make install

If you're running Linux, then always remember to do the following command after installing any library:

- sudo ldconfig

If you encounter "Cannot import gnuradio" error, then go to [Finding the Python library](https://wiki.gnuradio.org/index.php/ModuleNotFoundError#B._Finding_the_Python_library) to set your PYTHONPATH and LD_LIBRARY_PATH.
After setting these environment variables, you need to do `sudo ldconfig` again for the Linux dynamic library loader to find the just-installed GNU Radio libraries.
If you have installed in a custom path with `-DCMAKE_INSTALL_PREFIX=XXX`, you will need to add that path to $PATH in order to find gnuradio-companion. 

## SoapySDR

After GNURadio 3.8, gr-osmocom hasn't really been maintained.  This means that to use GNURadio 3.9 or newer, we need a different block to act as the interface between the SDR and GNURadio.  The best replacement right now is SoapySDR and the gr-sopay module.  

To build gr-soapy, follow the instructions at [gr-soapy](https://gitlab.com/librespacefoundation/gr-soapy) or read below:

```bash
apt-get install \
  libboost-dev \
  libboost-date-time-dev \
  libboost-filesystem-dev \
  libboost-program-options-dev \
  libboost-system-dev \
  libboost-thread-dev \
  libboost-regex-dev \
  libboost-test-dev \
  python3 \
  python3-six \
  python3-mako \
  python3-dev \
  swig \
  cmake \
  gcc \
  gnuradio-dev \
  libsoapysdr-dev \
  libconfig++-dev \
  libgmp-dev \
  liborc-0.4-0 \
  liborc-0.4-dev \
  liborc-0.4-dev-bin \
  git
```

```bash
git clone https://gitlab.com/librespacefoundation/gr-soapy
cd gr-soapy
mkdir build
cd build
cmake ..
make -j $(nproc --all)
sudo make install

```

This is only half the answer though.  To actually use a specific sdr with gr-soapy, you will need to install the soapy plugin for that sdr.  For example, to use a hackrf with soapy, you need the soapy hackrf plugin, which is built by:

```bash
git clone https://github.com/pothosware/SoapyHackRF.git
cd SoapyHackRF
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig

```

You will need to do this for every type of SDR you plan on using

## Other useful software

- [Inspectrum](https://github.com/miek/inspectrum) : useful for viewing RF captures
- [qspectrumanalyzer](https://github.com/xmikos/qspectrumanalyzer) : a easy way to turn an sdr into a spectrum analyzer
- [SDR#](https://airspy.com/download/) : A free windows only sdr package that acts as a replacement to gqrx