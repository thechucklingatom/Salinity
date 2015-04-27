import serial
import matplotlib.pyplot as plt
import time
import math
from time import sleep as zzz
import csv

#run as python3 -W ignore plot.py to supress the warnings.

#serial port for the aruduino at whatever frequency it was set to
#linux
ser = serial.Serial('/dev/ttyACM0', 9600)
#windows
#ser = serial.Serial('COM3', 9600)

#gets the starting time for the program changed time.clock() to time.time()
startTime = time.time()
#starting data point
line = ser.readline()
#converts to a number
dataInital = [float(val) for val in line.split()][0]

#initialize the lists and set the first value.
timeList = []
dataList = []
formula1List = []

#sets the initial stuff
timeList.append(startTime - startTime)
dataList.append(dataInital* (5/1023.0))
#since the % weight salinity shouldn't be above 26% I have a hard cap at that.
if math.exp(((dataInital * (5/1023.0)) - 2.9386)/ .1525) > .26:
    formula1List.append(.26 * 100)
else:
    formula1List.append(100 * math.exp(((dataInital * (5/1023.0)) - 2.9386) / .1525))
#here is where I make the plots/subplots
plt.subplot(211)
plt.ylabel("Voltage")
plt.plot(timeList,dataList)
plt.subplot(212)
plt.ylabel("% Weight Salinity")
plt.plot(timeList,formula1List)
plt.xlabel("Time")
plt.show(block=False)

#for use later
loopControl = True

#ask for the file name
filename = input("What would you like to call the file? ")

#if the file opens, should 100% because w+
with open(filename + '.csv', 'w+', newline='') as csvFile:
    #tells how to write to the file
    testFile = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    #user control
    userInput = input("enter q to quit, r to read: ")

    #if they dont want to quit
    while userInput != 'q':
    	#initialize n
        n = 1
        numReads = 1
        if userInput == 'r':
            #if they want to read ask them how many times
            n = int(input("How many minutes do you want to read? "))
            numReads = int(input("How many times per minutes would you like to read "))
	#read data n times seperated by ~1 sec
        for i in range(1, (n*numReads)+1):
            #if you don't flush your input you will not read at the current time
            ser.flushInput()
            
            #loop to make sure it reads a data point
            while loopControl:
                #this is sometimes out of range if the board hasnt sent anything
                #so I read until I get something
                try:
                    #read the line
                    line = ser.readline()
                    #convert it to a float
                    data = [float(val) for val in line.split()][0] * (5/1023.0)
                    #this keeps the random spikes from happening, the off by a factor of 10 error
                    if data <= .5 or data > 3.4:
                        loopControl = True
                    else:
                        loopControl = False
                except:
                    #if something breaks try again
                    loopControl = True
            #add data to list to the list
            timeList.append((time.time() - startTime)/60)
            dataList.append(data)
            #again above .26 doesnt make sense
            if math.exp((data - 2.9386) / .1525) > .26:
                formula1List.append(.26 * 100)
            else:
                formula1List.append(100 * math.exp((data - 2.9386) / .1525))
            #clear the plot
            plt.clf()
            #add everything again
            plt.subplot(211)
            plt.ylabel("Voltage")
            plt.plot(timeList,dataList)
            plt.subplot(212)
            plt.ylabel("% Weight Salinity")
            plt.plot(timeList,formula1List)
            plt.xlabel("Time")
            #redraw it
            plt.draw()
            loopControl = True
            #print to console, not needed just for visual
            print(data)
            if i != n * numReads:
                #zzz(1 * 60)
                #this is used over the sleep because it keeps our plot from freezing
                #it works the same as sleep
                plt.pause(60/numReads)
        #check if they want to quit
        userInput = input("enter q to quit, r to read: ")
    #read final time
    finalTime = time.time()
    timeList.append((finalTime - startTime) / 60)
    #add it all to the csv file
    testFile.writerow(["Voltage","Time","%weight salinity"])
    testFile.writerows(zip(dataList, timeList,formula1List))
    testFile.writerow(["No data",timeList[-1],formula1List[-1]])
    #print running time for debug.
    print("%f:%f" % (startTime, finalTime))
#graph safety
input("Don't forget to save the graph, press enter to exit: ")
