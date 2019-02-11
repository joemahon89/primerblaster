

import subprocess
import configparser


def getconfig():
	config = configparser.ConfigParser()
	config.read('config.ini')
	return config

def main(config):
	# Load path for chromosome aliases and file containing primers
	# Load path for temporary fasta file
	tempfasta = config['DEFAULT']['temp_fasta_individual']
	# Load BLAST tool naclarid db path
	blast_path_tool = config['DEFAULT']['blast_path_tool']
	blast_path_db = config['DEFAULT']['blast_path_db']

	# Run BLAST on the temporary fasta file
	print("BLASTING", tempfasta)
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
		print(line)
	print("Note - No results are saved with this tool")



if __name__ == "__main__":
	config = getconfig()
	main(config)