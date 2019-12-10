import os 
import re
import csv
import itertools
import datetime as dt
import pandas as pd

# ordered 001 to 030 when a fable ends for a user per trial
end_of_fable = [[107, 234, 400], [97, 221, 376], [101, 223, 384], [126, 244, 410], [109, 238, 402] ,[109, 237, 391],
				[101, 233, 394], [113, 252, 383], [103, 235, 394], [118, 242, 378], [97, 245, 405], [97, 256, 420],
				[121, 259, 430], [100, 228, 448], [97, 259, 454], [125, 257, 445], [105, 234, 444], [112, 281, 471],
				[108, 233, 408], [105, 223, 381], [101, 233, 385], [107, 225, 372], [114, 234, 397], [115, 245, 407],
				[106, 236, 396], [103, 219, 391], [97, 215, 367], [105, 228, 414], [101, 236, 419], [124, 276, 438]]

user_list = list(itertools.chain.from_iterable(itertools.repeat(x, 3) for x in range(0,11)))

def Filter(ls): 
	return [str for str in ls if re.match(r'\d{4}-\d{3}-\d{3}.log', str)]

def FilterCSV(ls): 
	return [str for str in ls if re.match(r'\d{4}-\d{3}-\d{3}.csv', str)]

def to_dt(str_time):
	splits = str_time.split(':')
	hour = int(splits[0])
	minute = int(splits[1])
	second_split = splits[2].split('.')
	second = int(second_split[0])
	microsecond = int(second_split[1]) * 1000

	x = dt.datetime(1, 1, 1, hour=hour, minute=minute, second=second, microsecond=microsecond)

	return x

def append_data():
	lst = FilterCSV(os.listdir("data_clean"))
	lst.sort()
	print("Appending list of files:", lst)

	# read all cleaned data and append to one csv (while adding user and session info)
	full_csv = [pd.read_csv("data_clean/"+f) for f in lst]
	next_it = 0
	for ind, csv in enumerate(full_csv):
		if (ind)%3 == 0:
			next_it = 0
		else:
			next_it +=4
		csv.insert(0, "user", [str(user_list[ind])] * len(csv))
		# arguably the worst line of code I've ever written (I apologize)
		csv.insert(1, "session", ([str(next_it)] * (end_of_fable[ind][0]-1)) + ([str(next_it+1)] * ((end_of_fable[ind][1]-1)-(end_of_fable[ind][0]-1))) + ([str(next_it+2)] * ((end_of_fable[ind][2]-1)-(end_of_fable[ind][1]-1))) + ([str(next_it+3)] * ((len(csv)+1)-end_of_fable[ind][2])))
	full_csv = pd.concat(full_csv)

	# normalize timepress and timerelease to unique user + session
	grouped_times = full_csv.groupby(['user', 'session'])['timepress'].transform('first')
	full_csv['timepress'] = (full_csv['timepress'] - grouped_times)
	full_csv['timerelease'] = (full_csv['timerelease'] - grouped_times)

	full_csv.to_csv( "data_clean/full_data.csv", index=False, encoding='utf-8-sig')

def main():
	print("codey code code")

	files = sorted(Filter(os.listdir('data')))
	print(files)

	for file in files:

		f_r = open("data/"+file)
		f_r.readline()
		data =  [x[:-1] for x in f_r.readlines()]
		print(file)
		f_r.close()

		if os.path.exists("data_clean/"+file[:-4]+".csv"):
			os.remove("data_clean/"+file[:-4]+".csv")
		else:
			print("Can not delete the file as it doesn't exists")


		data_len = len([x for x in data if "pressed" in x])
		keep_idcs = list(range(data_len))
		temp = []

		for i, line in enumerate(data):
			current = line.replace(" special:", "").replace("Key.", "").replace("_r", ""). \
				replace("_l", "").lower().split(" ")
			current[1] = current[1].replace(',', '.')
			current[2] = current[2].replace(",", "comma")

			if current[3] == "pressed":
				for j in range(i+1, len(data)):
					current_inner = data[j].replace(" special:", "").replace("Key.", ""). \
						replace("_r", "").replace("_l", "").lower().split(" ")
					current_inner[1] = current_inner[1].replace(',', '.')
					current_inner[2] = current_inner[2].replace(",", "comma")

					if (current_inner[2] == current[2]):
						if current_inner[3] == "released":
							temp.append([current, current_inner])
							break
							

		prev_release = None
		first_press = to_dt(temp[0][0][1])
		cleaned = []
		for dat in temp:
			if dat[1] != prev_release:
				press = to_dt(dat[0][1])
				release = to_dt(dat[1][1])
				timepress = (press - first_press)
				timepress = 1000*timepress.seconds + int(timepress.microseconds/1000)

				diff = (release - press)
				diff = 1000*diff.seconds + int(diff.microseconds/1000)
				timerelease = timepress + diff				
				
				cleaned.append([dat[0][2], timepress, timerelease])
				prev_release = dat[1]


		with open("data_clean/"+file[:-4]+".csv", 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["keyname", "timepress", "timerelease"])
			writer.writerows(cleaned)

		print("file closed")

	append_data()

if __name__ == '__main__':
	main()