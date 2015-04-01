import serial
import matplotlib as plt
import time
from time import sleep as zzz
import csv

ser = serial.Serial('COM3', 9600)

startTime = time.clock()
line = ser.readline()
dataInital = [float(val) for val in line.split()][0]

timeList = []
dataList = []
timeList.append(startTime)
dataList.append(dataInital)

with open('data.csv', 'w', newline='') as csvFile:

	testFile = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	#testFile.writerow([dataInital, "%f" % (startTime)])

	userInput = input("enter q to quit, r to read: ")

	while userInput != 'q':
		n = 1
		if userInput == 'r':
			n = int(input("How many seconds do you want to read? "))
		for i in range(1, n):
			ser.write(b'1')
			line = ser.readline()
			timeList.append(time.clock())
			data = [float(val) for val in line.split()][0]
			dataList.append(data)
			print(data)
			zzz(1)
		userInput = input("enter q to quit, r to read: ")

	finalTime = time.clock()
	timeList.append(finalTime)
	testFile.writerows(zip(dataList, timeList))
	testFile.writerow(["No data",timeList[-1]])
	print("%f:%f" % (startTime, finalTime))