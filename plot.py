import serial
import matplotlib.pyplot as plt
import time
import math
from time import sleep as zzz
import csv

#serial port for the aruduino at whatever frequency it was set to
#linux
ser = serial.Serial('/dev/ttyACM0', 9600)
#windows
#ser = serial.Serial('COM3', 9600)

#gets the starting time for the program change time.clock() to time.time()
startTime = time.time()
#starting data point
line = ser.readline()
#converts to a number
dataInital = [float(val) for val in line.split()][0]

#initialize the lists and set the first value.
timeList = []
dataList = []
formula1List = []

timeList.append(startTime - startTime)
dataList.append(dataInital* (5/1023.0))
if math.exp(((dataInital * (5/1023.0)) - 2.9386)/ .1525) > .26:
    formula1List.append(.26 * 100)
else:
    formula1List.append(100 * math.exp(((dataInital * (5/1023.0)) - 2.9386) / .1525))
plt.subplot(211)
plt.ylabel("Voltage")
plt.plot(timeList,dataList)
plt.subplot(212)
plt.ylabel("% Weight Salinity")
plt.plot(timeList,formula1List)
plt.xlabel("Time")
plt.show(block=False)

loopControl = True

#ask for the file name
filename = input("What would you like to call the file? ")

#if the file opens
with open(filename + '.csv', 'w+', newline='') as csvFile:
    #tells how to write to the file
    testFile = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #testFile.writerow([dataInital, "%f" % (startTime)])

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
            ser.flushInput()
            #ser.write(b'1')
            #ser.flushInput()
            while loopControl:
                try:
                    line = ser.readline()
                    data = [float(val) for val in line.split()][0] * (5/1023.0)
                    if data <= .5 or data > 3.4:
                        loopControl = True
                    else:
                        loopControl = False
                except:
                    loopControl = True
            timeList.append((time.time() - startTime)/60)
            dataList.append(data)
            if math.exp((data - 2.9386) / .1525) > .26:
                formula1List.append(.26 * 100)
            else:
                formula1List.append(100 * math.exp((data - 2.9386) / .1525))
            plt.clf()
            plt.subplot(211)
            plt.ylabel("Voltage")
            plt.plot(timeList,dataList)
            plt.subplot(212)
            plt.ylabel("% Weight Salinity")
            plt.plot(timeList,formula1List)
            plt.xlabel("Time")
            plt.draw()
            loopControl = True
            print(data)
            if i != n * numReads:
                #zzz(1 * 60)
                plt.pause(60/numReads)
        #check if thy want to quit
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
