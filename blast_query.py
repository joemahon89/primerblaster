
import csv
import subprocess
import os
import configparser



def read_csv(file):
	""" Returns a dict created from the provided csv file, with
	primer name: primer sequence
	"""
	csvcontents = {}
	with open(file) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=",")
		for row in csv_reader:
			csvcontents[row[0]]=row[1]
	return csvcontents


def createlogfile(output_bed_file):
	""" If the log file does not already exist, create it """
	if os.path.isfile(output_bed_file):
		print("Adding to existing log file")
	else:
		print("Creating new log file")
		with open(output_bed_file, 'w') as file:
			os.utime(output_bed_file, None)

def append_output(output_bed_file, contents):
	""" Appends a single line to the output log file """
	with open(output_bed_file, 'a') as file:
		writer = csv.writer(file, delimiter="\t")
		writer.writerow(contents)

def create_temp_fasta(tempfasta, contents):
	""" Creates the temporary fasta file required for the BLAST tool to
	process.
	"""
	with open(tempfasta, 'w') as file:
		file.write(">"+contents[0]+"\n"+contents[1])


def alreadyfound(query, output_bed_file, contents):
	""" Uses the output_bed_file to check whether primer has already been BLASTed.
	Useful as allows continuation when BLASTing very large lists of primers.
	"""
	found = False
	output_bed_file = open(output_bed_file)
	lines = 0
	for line in output_bed_file:
		lines += 1
		if query in line:
			print(primer+" already BLASTED, skipping")
			found = True
	print(lines,"/",len(contents), "processed.")	
	return found


def main(config):
	""" Runs the main program """
	# Load path for chromosome aliases and file containing primers
	primerfile = config['DEFAULT']['primerfile']
	aliasfile = config['DEFAULT']['chromosome_aliases']
	# Load path for temporary fasta file
	tempfasta = config['DEFAULT']['temp_fasta']
	# Load BLAST tool and db path
	blast_path_tool = config['DEFAULT']['blast_path_tool']
	blast_path_db = config['DEFAULT']['blast_path_db']
	# Load path for the output file and create it if not present
	output_bed_file = config['DEFAULT']['output_bed_file']
	createlogfile(output_bed_file)

	contents = read_csv(primerfile)
	aliases = read_csv(aliasfile)

	for primer in contents:
		print("Currently processing", primer)
		# Process if not a blank line
		if contents[primer] != "":
			# Check whether the primer ID is already in the output_bed_file
			if alreadyfound(primer, output_bed_file, contents):
				pass
			else:
				# BLAST tool works with a fasta file as input, so a temporary
				# fasta file is created for each primer sequence and
				# overwritten each time
				create_temp_fasta(tempfasta, [primer, contents[primer]])

				# Run BLAST on the temporary fasta file
				results = subprocess.check_output([blast_path_tool, 
													'-db', blast_path_db,
													'-query', tempfasta, 
													'-task', 'blastn-short',
													'-num_threads','8',
													'-outfmt','7'])


				# BLAST tool returns raw text, so decode and extract top
				# result from output
				results = results.decode("utf-8")
				resultslines = results.split("\n")
				for line in resultslines:
					columns = line.split("\t")
					if columns[0] == primer:
						# BLAST returns chr transcript IDs instead of chr 
						# number so alias file used to convert
						chromosome = aliases[columns[1]]
						start = columns[8]
						end = columns[9]
						# Append the results of the BLAST query to the log file
						append_output(output_bed_file, [chromosome, start, end, primer])
						break


def getconfig():
	config = configparser.ConfigParser()
	config.read('config.ini')
	return config


if __name__ == "__main__":
	config = getconfig()
	main(config)

# def find_not_done(logfile, onestodo):
# 	csvcontents = []
# 	with open(logfile) as csvfile:
# 		csv_reader = csv.reader(csvfile, delimiter="\t")
# 		for row in csv_reader:
# 			csvcontents[row[0]]=row[1]
# 	return csvcontents
		