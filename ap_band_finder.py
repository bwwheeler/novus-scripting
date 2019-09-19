"""
Access Point Band Finder
Find the band capabilities of access points in one CSV based on the inventory records in a different CSV
So, it's not the most universal of scripts but it'll still save me time
Someday I will make a modified version of this that uses openpyxl

Input 1: CSV with access point names in the column 1
Input 2: CSV with 2.4GHz information in columns 3 and 4
"""

import os
import sys
import csv

def open_files(ap_list, inventory_list):
	''' Open input csv and output file (so as not to waste time if it's invalid or locked) '''
	try:
		intl_ap_file = open(ap_list)
		intl_ap_csv = csv.reader(intl_ap_file)
		intl_ap_csv_data = list(intl_ap_csv)
		intl_ap_file.close()
		
		inv_ap_file = open(inventory_list)
		inv_ap_csv = csv.reader(inv_ap_file)
		inv_ap_csv_data = list(inv_ap_csv)
		inv_ap_file.close()
		
	except FileNotFoundError:
		print ('File does not exist')
		exit()
		
	try:
		output_file = open(ap_list[:-4] + '_completed.csv', 'w', newline='')
	except FileNotFoundError:
		print('File', ap_list[:-4] + '_completed.csv', 'not found')
		exit()
	except PermissionError:
		print('Unable to write to', ap_list[:-4] + '_completed.csv')
		exit()
		
	return intl_ap_csv_data, inv_ap_csv_data, output_file

def find_band_data(intl_ap_csv_data, inv_ap_csv_data):
	'''Write the Intl AP list, adding band info for where that AP is present in Inv AP list'''
	intl_aps_with_bands = []
	for line in intl_ap_csv_data:
		temp_line = [line[0], line[1], line[2]]
		for inv_line in inv_ap_csv_data:
			if inv_line[1] == line[1]:
				temp_line.append(inv_line[2])
				temp_line.append(inv_line[3])
				break
		intl_aps_with_bands.append(temp_line)
	return intl_aps_with_bands
	
def write_csv(intl_aps_with_bands, output_file):
	'''Write a new csv using the output file opened earlier'''
	output_writer = csv.writer(output_file)
	output_writer.writerow(['Make','Model','Regional Market','2.4GHz','5GHz'])
	for line in intl_aps_with_bands:
		output_writer.writerow(line)
	print('File', output_file.name, 'written')
	output_file.close()

def main():
	intl_ap_csv_data, inv_ap_csv_data, output_file = open_files(sys.argv[1], sys.argv[2])
	csv_data_to_write = find_band_data(intl_ap_csv_data, inv_ap_csv_data)
	write_csv(csv_data_to_write, output_file)

if __name__ == "__main__":
	main()