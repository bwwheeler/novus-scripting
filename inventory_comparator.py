'''
Read list of Novus inventory numbers (one per line) and cross-reference with a (freshly exported!) Novus inventory list to find devices that are currently checked in.
This should be made more generic in order to take any list of inventory numbers; right now it's pretty messy
Just remember that lists are iterable, csv.reader objects are iterators!

input: list of inventory numbers, inventory csv
eg: inventory_comparator.py device_list.txt inventory.csv

to-do: better output formatting, any error handling whatsoever

'''

import csv
import sys

def main():
	device_status_list = []
	
	with open(sys.argv[1]) as devices:
		devices_list = devices.read().splitlines()
		with open(sys.argv[2], newline='') as inventory_csv:
			inventory_csv_list = list(csv.reader(inventory_csv))
			
			for device in devices_list:
				found = False
				for item in inventory_csv_list:
					if str(item[0]) == str(device):
						found = True
						device_status_list.append('{},{}\n'.format(device, item[3].lower()))
						break
				if not found:
					device_status_list.append('{},not found\n'.format(device))
						
	print(device_status_list)
		
	with open('device_status.csv','w') as device_file:
		for device in device_status_list:
			device_file.write(device)
			
if __name__ == "__main__":
	main()