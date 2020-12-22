#!/usr/bin/env python

"""
Copyright(C) 2020, BrucesHobbies
All Rights Reserved

AUTHOR: BruceHobbies
DATE: 12/22/2020
REVISION HISTORY
  DATE        AUTHOR          CHANGES
  yyyy/mm/dd  --------------- -------------------------------------


OVERVIEW:
    This program plots temperatures and humidity from the CSV files 
    generated by sdrWeatherStn.py

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

INSTALLATION:
Requires:
   sudo pip3 install matplotlib

"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import math
import time
import datetime
import csv


stationFilenames = ["Acurite-Tower Id nnnn Ch C.csv","Ambientweather-F007TH Id nn Ch 1.csv","Ambientweather-F007TH Id nn Ch 2.csv"]
stationNames = ["Outdoor","Indoor","PumpHse"]


#
# Read in a comma seperated variable file. Assumes a header row exists.
#   Time series with time in seconds in first column.
#
def importCsv(filename) :
    print("Reading " + filename)

    with open(filename, 'r') as csvfile :
        data = list(csv.reader(csvfile))

    header = data[0]
    tStamp = []
    temp = []
    humidity = []

    if "temperature_C" in header :
        tIdx = header.index("temperature_C")
    elif "temperature_F" in header :
        tIdx = header.index("temperature_F")
    else :
        tIdx = 0
            
    if "humidity" in header :
        hIdx = header.index("humidity")
    else :
        hIdx = 0

    for row in data[1:] :
        tStamp.append(float(row[0]))
        temp.append(float(row[tIdx]))
        humidity.append(float(row[hIdx]))

    return header, tStamp, temp, humidity


#
# Plot
#
def plotSingle(t, var, ylabel, title) :
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.plot(t, var)
    # ax1.plot(t, var, marker='d')

    ax1.set_title(title)
    ax1.set_xlabel('Time')
    ax1.set_ylabel(ylabel)
    
    # ax1.legend(loc='upper right', shadow=True)
    ax1.grid(which='both')
    plt.gcf().autofmt_xdate()    # slant labels
    dateFmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
    plt.gca().xaxis.set_major_formatter(dateFmt)

    plt.show(block=False)


#
# Plot the files
#
if __name__ == "__main__" :

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1, 1, 1)
    ax1.set_title("Temperature")
    ax1.set_xlabel('Time')
    ax1.set_ylabel("Temp Degrees")
    ax1.grid(which='both')
    plt.gcf().autofmt_xdate()    # slant labels
    dateFmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
    plt.gca().xaxis.set_major_formatter(dateFmt)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1, 1, 1)
    ax2.set_title("Humidity")
    ax2.set_xlabel('Time')
    ax2.set_ylabel("Percentage RH")
    ax2.grid(which='both')
    plt.gcf().autofmt_xdate()    # slant labels
    dateFmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
    plt.gca().xaxis.set_major_formatter(dateFmt)

    for i in range(len(stationFilenames)) :
        header, tStamp, temp, humidity = importCsv(stationFilenames[i])

        t = [datetime.datetime.fromtimestamp(ts) for ts in tStamp]

        if True :
            if "temperature_C" in header :
                for k in range(len(temp)) :
                    temp[k] = round(temp[k] * 9.0 / 5.0 + 32.0, 1)
        else :
            if "temperature_F" in header :
                for k in range(len(temp)) :
                    temp[k] = round((temp[k] - 32.0) * 5.0 / 9.0, 1)

        ax1.plot(t, temp, label=stationNames[i])
        ax2.plot(t, humidity, label=stationNames[i])

    ax1.legend(loc='upper right', shadow=True)
    ax2.legend(loc='upper right', shadow=True)
    plt.show(block=False)

    # Pause to close plots
    input("Press [enter] key to close plots...")
    print("Done...")