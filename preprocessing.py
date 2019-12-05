import os 
import re
import csv

def Filter(ls): 
    return [str for str in ls if re.match(r'\d{4}-\d{3}-\d{3}.log', str)] 

def main():
	print("codey code code")

	files = Filter(os.listdir('data'))
	print(files)

	for file in files:

		f_r = open("data/"+file)
		f_r.readline()
		data =  [x[:-1] for x in f_r.readlines()]
		print(file)
		f_r.close()
		#print(data)

		if os.path.exists("data_clean/"+file[:-4]+".csv"):
			os.remove("data_clean/"+file[:-4]+".csv")
		else:
			print("Can not delete the file as it doesn't exists")

		#f_w = open("data/"+file[:-4]+".csv","a+")
		#f_w.write("session, date, press, release, identity\n")

		temp = [None]*len([x for x in data if "pressed" in x])
		pointer = 0

		for line in data:
			#print(line)
			current = line.replace(" special:", "").replace(",", ".").split(" ")
			#print(current)
			if current[3] == "pressed":
				temp[pointer] = current[:-1]
				pointer += 1
			else:
				try:
					check = pointer - 1
					while(len(temp[check]) != 3 and temp[check][2].lower() != current[2].lower()):
						check = check - 1
					temp[check].insert(2, current[1])
				except:
					print("uh oh, no release")
		
		#for keystroke in temp:
		#	print(", ".join(keystroke))
		#	f_w.write(", ".join(keystroke)+"\n")

		with open("data_clean/"+file[:-4]+".csv", 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["date", "press", "release", "identity"])
			writer.writerows(temp)

		#f_w.close()
		print("file closed")
		#print(temp)

if __name__ == '__main__':
	main()