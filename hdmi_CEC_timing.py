import sys
import os
from datetime import datetime

#Example launch command:
# 1st argument must be a logcat output from a device connected to TV via HDMI

def scanLogcat():
	#relevant logcat codes defined by client
	relevantCodes = ["KEYCODE_HOME down=true","KEYCODE_HOME down=false","HdmiCecLogging: 40:0D","HdmiCecLogging: 04:90:00","HdmiCecLogging: 0F:80","HdmiCecLogging: 0F:86"]
	startTime = None

	try:
		logcatFile = open(sys.argv[1])
		logcatLines = logcatFile.readlines()

	except FileNotFoundError:
		print ('File', sys.argv[1], 'does not exist')
		exit()
		
	try:
		#Line interpretation goes here
		for line in logcatLines:
			#not exactly sure how this works
			if any(s in line for s in relevantCodes):
				#output timestamp and log, omit thread info
				if relevantCodes[0] in line:
					#set a start time to when the remote home button is print
					startTime = datetime.strptime(line[0:17], "%m-%d %H:%M:%S.%f")
					print ("0:00:00.000000: ", line[33:])
				else:
					#ignore HDMI events before home button is pressed
					if startTime is not None:
						eventTime = datetime.strptime(line[0:17], "%m-%d %H:%M:%S.%f")
						timeElapsed = eventTime - startTime
						#print time delta between home button press and other events in standard datetime format
						print (timeElapsed, ": ", line[33:])

	except KeyboardInterrupt:
		print ('User has pressed ctrl+c, closing script')
		logcatFile.close()
		exit()

def main():
	scanLogcat()

if __name__== "__main__":
  main()
