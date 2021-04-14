# sdrWeatherStn
Software Defined Radio (SDR) Weather Station
Copyright(C) 2020, BrucesHobbies,
All Rights Reserved

sdrWeatherStn.py records any 433 MHz data it recognizes from a low-cost Software Defined Radio (SDR) USB dongle such as the NooElec R820T which are about $20 USD. If your country uses a different frequency than 433 MHz, you can update the frequency in the Python script. The program logs each sensor to a separate Comma Separated Variable (csv) file with the option of throttling the data to every 15 minutes or custom time intervals. The program automatically generates a header row for each sensor log file with the appropriate labels for the data that will be logged. The program also logs some types of security sensors, smoke detectors, car tire pressure monitoring sensors including id, etc. Logs can be analyzed in a spreadsheet program or using MatPlotLib. publishData.py is for you to customize the alerts or to add interfaces like Blynk, Twilo, MQTT, etc. - This is a DIY project for the Raspberry Pi or similar system using an inexpensive RTL-SDR. The software is written in Python and runs under Linux.
# sdrWeatherStn™ Project Overview
I had a pump house and workshop where I don't run the heat normally. I wanted to track the temperature and humidity levels to prevent frozen pipes and black mold. Heating in the pump house is from a single heat lamp and I didn't want to think about the damage if the bulb should burn out in the middle of sub-freezing night. I purchased a weather station to monitor the out buildings and was very impressed with the 433 MHz wireless range but clearing minimum and maximum temps/humidity, and alarm programming were not so user friendly using a magic sequence with only 3 buttons. It just seemed natural to see if I could use the RPI with a Software Defined Radio (SDR) to pick up the temperature and humidity readings and define my own custom alerts along with logging all the data.
Using a SDR on the RPI, I was able to pick up Ambient Weather, Acurite, and LaCrosse weather stations. To get a complete list of devices supported list under the latest version:

    rtl_433 -R


![Figure 1: RPI with SDR](https://github.com/BrucesHobbies/sdrWeatherStn/blob/main/figures/Figure1.PNG)

Figure 1: RPI with SDR

![Figure 2: Ambient Weather Station and Outdoor Temperature / Humidity Sensor](https://github.com/BrucesHobbies/sdrWeatherStn/blob/main/figures/Figure2.PNG)

Figure 2: Ambient Weather Station and Outdooor Temperature / Humidity Sensor

![Figure 3: Acurite Temperature / Humidity Sensor](https://github.com/BrucesHobbies/sdrWeatherStn/blob/main/figures/Figure3.PNG)

Figure 3: Acurite Temperature / Humidity Sensor

![Figure 4: LaCrosse Outdoor Temperature / Humidity Sensor](https://github.com/BrucesHobbies/sdrWeatherStn/blob/main/figures/Figure4.PNG)

Figure 4: LaCrosse Outdoor Temperature / Humidity Sensor

The program runs from a terminal window or at boot. If run from a terminal window the status screen is as shown below:

    2020-12-21 15:30:00 Ambientweather-F007TH Id nnn Ch 1 Temperature 70.8F Humidity 37
    2020-12-21 15:30:01 Ambientweather-F007TH Id nnn Ch 1 Temperature 70.8F Humidity 37

![Figure 5: Temperature Plot](https://github.com/BrucesHobbies/sdrWeatherStn/blob/main/figures/Figure_5.PNG)

Figure 5: Temperature Plot

![Figure 6: Humidity Plot](https://github.com/BrucesHobbies/sdrWeatherStn/blob/main/figures/Figure_6.PNG)

Figure 5: Humidity Plot

# Required Hardware 
As an Amazon Associate I earn a small commission from qualifying purchases. It does not in any way change the prices on Amazon. I appreciate your support, if you purchase using the links below.
## Software Define Radio (about $25 USD)
- [NooElec SDR](https://amzn.to/3mEoJYY)

## One or more of these weather sensors
The base stations are not needed but nice to have as a second display.

- [Ambient Weather Remote Sensors](https://amzn.to/34A0Dsi)

- [Ambient Weather Wireless Thermo-Hydrometer](https://amzn.to/34yTcl4)

- [Acurite Wireless Outdoor Temperature and Humidity Sensor](https://amzn.to/38osGMu)

- [LaCrosse Wireless Outdoor Thermo Hygrometer Transmitting Sensor](https://amzn.to/2KGERvQ)

## Raspberry Pi system (if you don’t already own one)
- Raspberry Pi (any of the following)
  - RPI-Zero
  - RPI 3B+
  - RPI 4B
- Power adapter for your Raspberry Pi
- Heatsinks (optional)
- SD-Card

For installing the Raspberry Pi operating system, you may want a USB keyboard and USB mouse along with an HDMI cable and monitor. If using the RPI4, a Micro-HDMI to HDMI adapter may be needed. It is possible to install the operating system without a keyboard, mouse, and monitor, but simpler is sometimes better. Once installed and configured you may want to switch to SSH or remote desktop so that you can remove the monitor, mouse, and keyboard.

# Software Installation
## Step 1: Setup the Raspberry Pi Operating System.
Here are the instructions to install the Raspberry Pi Operating System. [Raspberry Software Install Procedure](https://www.raspberrypi.org/software/operating-systems/)

Before continuing make sure your operating system has been updated with the latest updates.

    sudo apt-get update
    sudo apt-get upgrade
    sudo reboot now

## Step 2: Clone or install rtlsdr, rtl_433, etc.

    sudo apt-get install git libtool libusb-1.0.0-dev librtlsdr-dev rtl-sdr cmake automake python3 python3-pip
    sudo git clone https://github.com/merbanan/rtl_433.git
    cd rtl_433/
    sudo mkdir build
    cd build
    sudo cmake ..
    sudo make
    sudo make install
    cd ~

## Step 3: Install matplotlib
Matplotlib is used for plotting temperature and humidity:

    sudo pip3 install matplotlib

## Step 4: Download sdrWeatherStn software
There are 3 python files. To get a copy of the source files type in the following git command assuming you have already installed git:

    git clone https://github.com/BrucesHobbies/sdrWeatherStn

# Future Alert and Status Options
Please feel free to fork and contribute or provide feedback on priorities and features. I have an email / SMS alert that I want to clean up and include. Other possible additions are:

- Relay / buzzer
- MQTT
  - OpenHab
  - Home Assistant
  - Domoticz
- Blynk
- IFTT
- PubNub
- Twilio
- Cellular
- APRS

# Running
Just simply type the following from a terminal window:

    python3 sdrWeatherStn.py
    
To plot the data, edit the csv file list in the Python script and then run:

    python3 plotTempHumidity.py

# Auto Start at Boot
Type the following command:

    sudo crontab –e
    
Select the type of editor you are familiar with. I used nano. Add the following line at the end of the file and then press ctrl+O to write the file and ctrl+X to exit the nano editor.

    @reboot sleep 60 && cd sdrWeatherStn && python3 sdrWeatherStn.py

# Feedback
Let me know what you think of this project and any suggestions for improvements. Feel free to contribute to this open source project.
