#!/usr/bin/env python

"""
Copyright(C) 2020, BrucesHobbies
All Rights Reserved

AUTHOR: BrucesHobbies
DATE: 12/21/2020
REVISION HISTORY
  DATE        AUTHOR          CHANGES
  yyyy/mm/dd  --------------- -------------------------------------


OVERVIEW:
    sdrWeatherStn.py records any 433 MHz data it recognizes from a low-cost
      Software Defined Radio (SDR) USB dongle such as the R820T. If your 
      country uses a different frequency, you can update the Python script.
    Logs each sensor to a separate Comma Separated Variable (csv) file 
      with the option of throttling the data to every 15 minutes or 
      custom time intervals. Logs can be analyzed in a spreadsheet program
      or using MatPlotLib
    publishData.py is for you to customize the alerts or to add interfaces 
      like Blynk, Twilo, MQTT, etc.

LICENSE:
    This program code and documentation are for personal private use only. 
    No commercial use of this code is allowed without prior written consent.

    This program is free for you to inspect, study, and modify for your 
    personal private use. 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

INSTALL:
Make sure Raspberry Pi OS is current:
sudo apt-get update
sudo apt-get upgrade
sudo reboot now

Clone or install rtlsdr, rtl_433, etc.:
sudo apt-get install git libtool libusb-1.0.0-dev librtlsdr-dev rtl-sdr cmake automake python3 python3-pip
sudo git clone https://github.com/merbanan/rtl_433.git
cd rtl_433/
sudo mkdir build
cd build
sudo cmake ..
sudo make
sudo make install
cd ~

Clone this program:
sudo git clone https://github.com/bruceshobbies/sdrWeatherStn

Run command:
python sdrWeatherStn.py

"""


import os
import sys
import subprocess
import time
import datetime
import signal
import json

import publishData

encoding = 'utf-8'

#
# === USER CONFIGURATION SECTION ===
#

# Select prefered temp units for terminal display
# TEMP_UNITS = ''     # Native units
# TEMP_UNITS = 'C'    # Convert to degrees C
TEMP_UNITS = 'F'      # Convert to degrees F
MODE = 'terminal'     # display in terminal window

LOGGING_ENABLED = 1
T_LOGGING_INTERVAL = 15*60      # Throttle data logging (seconds) 15*60 recommended
                                # zero logs all

#
# === END USER CONFIGURATION SECTION ===
#

# Sensors discovered
sensors = {}


#
# Startup rtl_433 as a subprocess
#
def sdrInit() :
    # optional rtl_433 configuration
    """
    sampleRate = '5000'
    frequency = '433920000'
    cmd = "rtl_433 -s " + sampleRate + " -f " + frequency + "rtl_433 -F json 2>&1"
    """

    # Start rtl_433
    cmd = "rtl_433 -F json 2>&1"

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return p


#
# Read sdr data
#
def sdrRead(p) :
    pubData = 0

    if p.poll() is None:
        out = p.stdout.readline().decode(encoding)

        try :
            data = json.loads(out)
            # print("JSON: " + out)

            if "time" in data :
                dsplyStr = data["time"] + " "
                sensorTime = datetime.datetime.strptime(data["time"], '%Y-%m-%d %H:%M:%S')
                sensorUnixTime = time.mktime(sensorTime.timetuple())
            else :
                dsplyStr = ""
                sensorUnixTime = 0

            if "model" in data :
                sensorName = data["model"]
            else :
                sensorName = ""

            if "id" in data:
                sensorName += " Id " + str(data["id"])

            if "channel" in data :
                sensorName += " Ch " + str(data["channel"])

            dsplyStr += sensorName

            if "battery_ok" in data :
                if data["battery_ok"] == 0:
                    dsplyStr += ' Low Battery!'

            if "temperature_C" in data :
                pubData = 1
                tempValue = data["temperature_C"]
                if TEMP_UNITS == 'F' :
                    tempValue = round(tempValue*9.0/5.0+32.0,1)
                    dsplyStr += ' Temperature ' + str(tempValue)  + "F"
                else :
                    dsplyStr += ' Temperature ' + str(tempValue) + "C"

            if "temperature_F" in data :
                pubData = 1
                tempValue = data["temperature_F"]
                if TEMP_UNITS == 'C' :
                    tempValue = round((tempValue-32.0)*5.0/9.0,1)
                    dsplyStr += ' Temperature ' + str(tempValue) + "C"
                else :
                    dsplyStr += ' Temperature ' + str(tempValue) + "F"

            if "humidity" in data :
                pubData = 1
                rhValue = data["humidity"]
                dsplyStr += ' Humidity ' + str(rhValue)
            else :
                rhValue =[]

            if MODE == 'terminal' :
                print(dsplyStr)

            if LOGGING_ENABLED :
                csvAppend(sensorUnixTime, sensorName, data)

            if pubData :    # Must have temperature or humidity
                publishData.publishData(sensorUnixTime, sensorName, data, tempValue, rhValue)

        except :
            print(out)
            # pass


#
# Log each sensor to a separate Comma Separated Variable (*.CSV) log file to import to a spreadsheet
#    or plot using python MatPlotLib
#
def csvAppend(sensorUnixTime, sensorName, data) :
    global sensors

    # throttling - sensors may retransmit same information multiple times and at high rate
    if sensorName in sensors :
        t, d = sensors[sensorName]

        if (sensorUnixTime >= T_LOGGING_INTERVAL + t) or (T_LOGGING_INTERVAL == 0) :
            logCmd = 1
        else :
            logCmd = 0
    else :
        logCmd = 1

    if logCmd :
        sensors[sensorName] = [sensorUnixTime, data]

        logFilename = sensorName + ".csv"

        if not os.path.isfile(logFilename) :
            # If csv log file does not exist, write header
            hdr = "UnixTime (s)"
            for item in data :
                hdr += "," + item
        else :
            hdr = ""

        d = str(sensorUnixTime)
        for item in data :
            d += "," + str(data[item])

        with open(logFilename, "a") as csvFile :
            if hdr != "" :
                csvFile.write(hdr + "\n")
            csvFile.write(d + "\n")
            csvFile.close()


#
# main()
#
if __name__ == "__main__" :
    if MODE == 'terminal' :
        print("\nPress CTRL+C to exit...\n")

    p = sdrInit()

    try :
        while True :
            sdrRead(p)

    except KeyboardInterrupt :
        print("KeyboardInterrupt has been caught.")

    print('Ending rtl_433 subprocess...')
    p.kill()
    print("Done...")
