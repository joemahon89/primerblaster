
import csv
from pprint import pprint
import os

def createlogfile(logfile):
	if os.path.isfile(logfile):
		print("Adding to existing log file")
	else:
		print("Creating new log file")
		with open(logfile, 'w') as file:
			file.write("LOGFILE \n")


def write_csv_line(csv_file_path, line):
	with open(csv_file_path, 'a') as file:
		 writer = csv.writer(file, delimiter=",")
		 writer.writerow(line)



def find_not_done(logfile, primerfile):
	logcontents = []
	primerfilecontents = []
	# Logfile
	with open(logfile) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter="\t")
		for row in csv_reader:
			logcontents.append(row)
	# Primerfile
	with open(primerfile) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=",")
		for row in csv_reader:
			primerfilecontents.append(row)
	return logcontents, primerfilecontents


logfile = "log.txt"
primerfile = "Primers_without_tags_2007_on.csv"

logcontents, primerfilecontents = find_not_done(logfile, primerfile)

matches = 0
nomatches = 0
notfound = []
for i in primerfilecontents:
	#print(len(i))
	if len(i[0]) >0:
		found = False
		for j in logcontents:
			#print("i", i)
			#print("j", j)
			if i[0] == j[0]:
				found = True
			else:
				pass
		if found == True:
			matches +=1
		else:
			nomatches +=1
			if len(i[1]) == 0:
				notfound.append([i[0], "NO SEQUENCE IN ORIGINAL DATASET"])
			elif "*" in i[1]:
				notfound.append([i[0], "ASTERIX IN ORIGINAL SEQUENCE"])
			elif i[1][0] in ["A", "C", "T", "G", "a", "t", "c", "g"] and i[1][1] in ["A", "C", "T", "G", "a", "t", "c", "g"]:
				notfound.append([i[0], "NO BLAST RESULTS"])
			else:
				notfound.append([i[0], i[1]])
pprint(notfound)
print("Matches:", matches)
print("No matches:", nomatches)

nomatches = "nomatches.csv"

createlogfile(nomatches)
print("Writing log file contents")
for i in notfound:
	write_csv_line(nomatches, i)
