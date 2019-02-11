


import subprocess

results = subprocess.check_output(['/home/jmahon/software/blast/ncbi-blast-2.8.1+/bin/blastn', '-db', '/media/sf_Q_DRIVE/DNA/simonb/Labhelper_References/blastdb/grch37p13.blast', '-query', '/media/sf_F_DRIVE/Projects/blastquery_ian/individual.fa', '-task', 'blastn-short','-num_threads','8','-outfmt','7'])

print(results)