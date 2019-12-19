import csv 

def main():
	with open('data_clean/full_data.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		first = 0
		for row in spamreader:
			if first == 0:
				print("first row")
			else:	
				if(int(row[4])-int(row[3]) <= 0):
					print(row)
			first += 1

if __name__ == '__main__':
	main()