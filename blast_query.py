
import csv
import subprocess
import time
import os

primerfile = "Primers_without_tags_2007_on.csv"


logfile = "log.txt"
tempfasta = "test.fa"
aliasfile = "hg19_alias.csv"



def read_csv(file):
	csvcontents = {}
	with open(file) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=",")
		for row in csv_reader:
			csvcontents[row[0]]=row[1]
	return csvcontents

def print_primer_csv(contents):
	for i in contents:
		print(i, contents[i])

def createlogfile(logfile):
	if os.path.isfile(logfile):
		print("Adding to existing log file")
	else:
		print("Creating new log file")
		with open(logfile, 'w') as file:
			file.write("LOGFILE \n")

def append_log(logfile, contents):
	with open(logfile, 'a') as file:
		 file.write(contents+"\n")

def create_temp_fasta(tempfasta, contents):
	with open(tempfasta, 'w') as file:
		file.write(">"+contents[0]+"\n"+contents[1])


def alreadyfound(query, logfile, contents):
	found = False
	logfile = open(logfile)
	lines = 0
	for line in logfile:
		lines += 1
		if query in line:
			print(primer+" already done, skipping")
			print(line.strip())
			found = True
			
	print(lines,"/",len(contents))	
	return found

contents = read_csv(primerfile)
aliases = read_csv(aliasfile)

for primer in contents:
	print("currently processing line", primer)
	if contents[primer] != "":
		if alreadyfound(primer, logfile, contents):
			pass
		else:
			create_temp_fasta(tempfasta, [primer, contents[primer]])
			time_start = time.time()
			results = subprocess.check_output(['/home/jmahon/software/blast/ncbi-blast-2.8.1+/bin/blastn', '-db', '/media/sf_Q_DRIVE/DNA/simonb/Labhelper_References/blastdb/grch37p13.blast', '-query', '/media/sf_F_DRIVE/Projects/blastquery_ian/test.fa', '-task', 'blastn-short','-num_threads','8','-outfmt','7'])
			time_end = time.time()
			time_total = time_end - time_start
			results = results.decode("utf-8")
			resultslines = results.split("\n")
			for line in resultslines:
				columns = line.split("\t")

				if columns[0] == primer:
					chromosome = aliases[columns[1]]
					start = columns[8]
					end = columns[9]
					#print(primer, chromosome, start, end, time_total)
					print(primer, chromosome, start, end)
					append_log(logfile, "\t".join([primer, chromosome, start, end]))
					break



# def find_not_done(logfile, onestodo):
# 	csvcontents = []
# 	with open(logfile) as csvfile:
# 		csv_reader = csv.reader(csvfile, delimiter="\t")
# 		for row in csv_reader:
# 			csvcontents[row[0]]=row[1]
# 	return csvcontents
		
		



# time_start = time.time()
# proc = subprocess.check_output(['/home/jmahon/software/blast/ncbi-blast-2.8.1+/bin/blastn', '-db', '/media/sf_Q_DRIVE/DNA/simonb/Labhelper_References/blastdb/grch37p13.blast', '-query', '/media/sf_F_DRIVE/Projects/blastquery_ian/test.fa', '-task', 'blastn-short','-num_threads','8','-outfmt','7'])
# time_end = time.time()





#print(len(contents))





# newproc = proc.decode("utf-8")
# print(newproc)
# print("Time taken:", time_end-time_start)




"""
Hi both
I have a problem which I think probably has an easy solution, I just don’t 
know what it is.  Can you help. I have a data file (attached) with ~1800 
short sequences (primers) attached.  All I need to do is a run a bulk “BLAST”
query on each sequence, to return ONLY the top 100% hit (or, plausibly,
separate entries for each 100% hit - but only the top hit would do), and
ONLY the chr, start and stop coordinate (such that it can be turned into a 
BED file).

So I am looking to go from
 
2007.247              ACTTGGGTTGTCCAATCAGC
 
To
 
2007.247              chr8       94767059             94767078
 
This will allow us to put all the primers from the primer database onto Alamut 
(and actually theoretically ultimately to put the bulk file back into another 
primer design tool/database or whatever so they’re saved programmatically for 
posterity), which will save the scientists loads of time looking up whether we 
have primers when we detect a variant that needs a confirmation, so it’s 
feasibly a big efficiency step. Any ideas how to do this?  I thought a big BLAST
query would work, but I only want the top 100% hit and some additional data. 
“bwa fastmap” seems to be suggested by someone in stack exchange but I dunno 
how to do that.  I’m sure there must be a quick way?

It may also be useful (following discussion with Nick) to consider how primers 
designed and inputted into our primer DB (MS Access) can be automatically added 
to the bottom of this BED file using some sort of text file write code.  
We think we/Nick can probably cobble this together in VBA, so just converting 
the existing text/spreadsheet file I sent you is more pressing, but if there is 
a programmatic solution (even if means triggering the same piece of rapid code 
every time someone adds a primer to the DB which converts the DB format into BED 
and re-writes the BED file) that would also be nice.

"""

