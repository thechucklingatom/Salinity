import serial
import matplotlib.pyplot as plt
import time
from time import sleep as zzz
import csv

#serial port for the aruduino at whatever frequency it was set to
#linux
#ser = serial.Serial('/dev/ttyACM0', 9600)
#windows
#ser = serial.Serial('COM3', 9600)
#test for both
ser = serial.Serial(2, 9600)

#gets the starting time for the program
startTime = time.clock()
#starting data point
line = ser.readline()
#converts to a number
dataInital = [float(val) for val in line.split()][0]

#initialize the lists and set the first value.
timeList = []
dataList = []
timeList.append(startTime)
dataList.append(dataInital* (5/1023))
plt.plot(timeList,dataList)
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
                    data = [float(val) for val in line.split()][0] * (5/1023)
                    loopControl = False
                except:
                    loopControl = True
            timeList.append(time.clock())
            dataList.append(data)
            plt.clf()
            plt.plot(timeList,dataList)
            plt.draw()
            loopControl = True
            print(data)
            if i != n * numReads:
                #zzz(1 * 60)
                plt.pause(60/numReads)
        #check if thy want to quit
        userInput = input("enter q to quit, r to read: ")
    #read final time
    finalTime = time.clock()
    timeList.append(finalTime)
    #add it all to the csv file
    testFile.writerows(zip(dataList, timeList))
    testFile.writerow(["No data",timeList[-1]])
    #print running time for debug.
    print("%f:%f" % (startTime, finalTime))
