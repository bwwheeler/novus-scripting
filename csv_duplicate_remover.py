"""
CSV Duplicate Remover
Removes all duplicate values in a given column of a provided CSV file, 
and writes the results to a new CSV with a similar name

Input: a CSV file
Output: another CSV file with duplicates removed
"""

import os
import sys
import csv

def open_files(filename):
	''' Open input csv and output file (so as not to waste time if it's invalid or locked) '''
	try:
		input_file = open(filename)
		csv_file = csv.reader(input_file)
		csv_data = list(csv_file)
		input_file.close()
	except FileNotFoundError:
		print ('File', sys.argv[1], 'does not exist')
		exit()
		
	try:
		output_file = open(str(sys.argv[1])[:-4] + '_filtered.csv', 'w', newline='')
	except FileNotFoundError:
		print('File', sys.argv[1], 'not found')
		exit()
	except PermissionError:
		print('Unable to write to', str(sys.argv[1])[:-4] + '_filtered.csv')
		exit()
		
	return csv_data, output_file

def find_duplicates(csv_data, column):
	''' Check for duplicate values in provided column, and write the row to a new CSV file if it is not a duplicate '''
	string_list = []
	csv_data_to_write = []
	for line in csv_data:
		if line[column] not in string_list:	
			string_list.append(line[column])
			csv_data_to_write.append(line)
	return csv_data_to_write	

def write_csv(csv_data, output_file):
	'''Write a new csv using the output file opened earlier'''
	output_writer = csv.writer(output_file)
	for line in csv_data:
		output_writer.writerow(line)
	print('File', output_file.name, 'written')
	output_file.close()

def main():
	csv_data, output_file = open_files(sys.argv[1])
	csv_data_to_write = find_duplicates(csv_data, 1)
	write_csv(csv_data_to_write, output_file)

if __name__ == "__main__":
	main()
