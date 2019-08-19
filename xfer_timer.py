import time, sys, os, winsound

#check a directory to see how many files are in items, and loop until a provided number of files is reached
#designed to check file transfer times over a wireless network
#usage: >python xfer_timer.py [dir] [target number of files]

numFiles = 0
targetNumFiles = sys.argv[2]
testDir = sys.argv[1]

startTime = time.time()

while not len(os.listdir(testDir)) >= targetNumFiles:
	curTime = time.time()
	elapsedTime = curTime - startTime
	print(len(os.listdir(testDir)), "items backed up. Waiting for", int(elapsedTime), "seconds so far.")
	time.sleep(1)
	
endTime = time.time()
elapsedTime = endTime - startTime
print("...and, done.")
winsound.Beep(1000, 1000)
print("It only took", int(elapsedTime), "seconds.")
