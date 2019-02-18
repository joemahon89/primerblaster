
# primerblaster

A tool to obtain chromosomal start/stop locations for primers when provided with an input.


[Installation](#installation)
[Mass BLASTing Primers](#mass-blasting-primers)


## Installation
Clone this repository
```bash
git clone https://github.com/joemahon89/primerblaster.git
```
This tool uses the offline version of BLAST rather than the API (due to API rate limiting), and so requires a local installation of BLAST (tested with `ncbi-blast-2.8.1+` [instructions here](https://www.ncbi.nlm.nih.gov/books/NBK52640/) and a local blast database (e.g `grch37p13.blast`).  

The `config.ini` file should be edited to point to these files. Absolute paths should be used for the temporary fasta file, BLAST and BLAST database, but relative file paths are acceptable for other files.


## Mass BLASTing Primers
This tool was designed to obtain chromosomal start/stop locations for large numbers of primers by BLASTing their sequences.  
Input should be provided in CSV format, with primer identifier followed by sequence.
`input/example.csv`
```bash
2006.123,GCTTACTGAATGAATCTACTCTAATCC
2006.125,TCACAACTTCTCCATAACGTGC
```
Input files should be placed in the `input` folder and `config.ini` altered to point to the correct file.  
The program can be run with:
```bash
python3 blast_query.py
```
The program will through the input file and indivdually BLAST the sequences, appending the start and stop results to `output.bed` in the `output` folder. If large numbers of primers are being BLASTed at once, the program can be exited and restarted when convenient, as it will compare the input and output and only BLAST the missing ones.

Note: When there is no sequence provided, e.g.`PRIMERNAME,    ` or there are no BLAST results, the primer is skipped and not added to the BED file.