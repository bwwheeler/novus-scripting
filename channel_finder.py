"""
Channel Determinator
Finds and outputs the Wi-Fi channel of an AP based on the provided frequency of a test pass.
Also reports whether 2.4GHz or 5GHz channels were tested.

Input Format Assumed:
AP name,2.5GHz freq,5Ghz freq

Output format:
Name,2.4GHz,Channel Tested,5GHz,Channel Tested
AP1,Yes,1,Yes,36
AP2,Yes,11,No,N/A
etc...
"""

import os
import sys
import csv
FREQ_TO_CHANNEL_24 = {'': 'N/A', 'N/A': 'N/A', '2412': '1', '2417': '2', '2422': '3', '2427': '4', '2432': '5', '2437': '6', '2442': '7', '2447': '8', '2452': '9', '2457': '10', '2462': '11'}
FREQ_TO_CHANNEL_5 = {'': 'N/A', 'N/A': 'N/A', '5180': '36', '5200': '40', '5240': '48', '5280': '56', '5300': '60', '5500': '100', '5580': '116', '5745': '149', '5765': '153', '5785': '157', '5805': '161', '5825': '165'}

def open_files(filename):
''' Open input csv (from testing) and output file (so as not to waste time if it's invalid or locked) '''
	try:
		ap_file = open(filename)
		csv_file = csv.reader(ap_file)
		ap_data = list(csv_file)
		ap_file.close()
	except FileNotFoundError:
		print ('File', sys.argv[1], 'does not exist')
		exit()
		
	try:
		output_file = open(sys.argv[2], 'w', newline='')
	except FileNotFoundError:
		print('File', sys.argv[2], 'not found')
		exit()
	except PermissionError:
		print('Unable to write to', sys.argv[2])
		exit()
		
	return ap_data, output_file

def find_channels(ap_data):
'''Write the AP/channels list by converting from WLAN frquency to channel based on dictionary constants'''
	aps_with_channels = []
	for line in ap_data:
		temp_line = [line[0]]
		try:
			temp_line.append(FREQ_TO_CHANNEL_24[line[1]])
			temp_line.append(FREQ_TO_CHANNEL_5[line[2]])
		except KeyError:
			print('Frequencies', line[1], 'and/or', line[2], 'not in dictionary')
			exit()
		aps_with_channels.append(temp_line)
	return aps_with_channels

def format_csv(aps_with_channels):
'''Format data into the final csv format, including columns indicating whether the AP being processed was dual-band'''
	csv_data = []
	for ap in aps_with_channels:
		try:
			csv_line = [ap[0]]
			if ap[1] != "N/A":
				csv_line.append("Yes")
			else:
				csv_line.append("No")
			
			csv_line.append(ap[1])
			
			if ap[2] != "N/A":
				csv_line.append("Yes")
			else:
				csv_line.append("No")
			
			csv_line.append(ap[2])
		except IndexError:
			continue
			
		csv_data.append(csv_line)
	return csv_data

def write_csv(csv_data, output_file):
'''Write the actual csv using the output file opened earlier'''
	output_writer = csv.writer(output_file)
	output_writer.writerow(['AP Name','2.4GHz','Channel Tested','5GHz','Channel Tested'])
	for line in csv_data:
		output_writer.writerow(line)
	print('File', sys.argv[2], 'written')
	output_file.close()
	return None

def main():
	ap_data, output_file = open_files(sys.argv[1])
	aps_with_channels = find_channels(ap_data)
	csv_data = format_csv(aps_with_channels)
	write_csv(csv_data, output_file)
	
if __name__ == "__main__":
	main()
