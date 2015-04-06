import serial
import matplotlib as plt
import time
from time import sleep as zzz
import csv

#serial port for the aruduino at whatever frequency it was set to
ser = serial.Serial('COM3', 9600)

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
dataList.append(dataInital)

#if the file opens
with open('data.csv', 'w', newline='') as csvFile:
	#tells how to write to the file
	testFile = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	#testFile.writerow([dataInital, "%f" % (startTime)])

	#user control
	userInput = input("enter q to quit, r to read: ")

	#if they dont want to quit
	while userInput != 'q':
		#initialize n
		n = 1
		if userInput == 'r':
			#if they want to read ask them how many times
			n = int(input("How many seconds do you want to read? "))
		#read data n times seperated by ~1 sec
		for i in range(1, n):
			ser.flushInput()
			ser.write(b'1')
			#ser.flushInput()
			line = ser.readline()
			timeList.append(time.clock())
			data = [float(val) for val in line.split()][0] * (5/1023)
			dataList.append(data)
			print(data)
			zzz(1)
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