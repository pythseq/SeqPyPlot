## Synopsis

SeqPyPlot is a program for plotting time series data. Data is formatted in to a tab delimeted text file and then fed in to the main script. The script accesses code stored in SeqPyPlotLib and generates plots for the input data, saving them to .png and .svg files. 

## Motivation

The program was originally written to plot output from the Cufflinks suite. A pipeline was created where RNA-seq data would be mapped, quantified, and then normalized together to allow for comparisons between samples. This ouptput was then formatted and fed in to SeqPyPlot to plot expression values for lists of genes. 

## Installation

You can either clone the repository, download the scripts, or copy the code in to new files.

## Dependencies

This program imports Numpy and MatPlotLib.

## Contributors

I am currently the only contributor t this project, but if you'd like to contribute, by all means please do. Let me know so I can include you here if you wish.

## License

This is free to use OpenSource software. Public Domain.

## Code Example - Typical Usage


 >$ python SeqPyPlot.py -t e12,e13,e14,e15 -o Dev_genes -c Control,Mutant genelist.txt plotter_data.txt


Output will be a folder named "Dev_genes" with files containing plot with a maximum of six plots per file.

## Full usage

First make sure that all of the programs files are in the same directory. Then run the script:

![Alt text](image/Full_usage_combined.png?raw=true "Full Usage")


 

## The run Script

In the run script, SeqPyPlot.py, you should aim to first read in any command line argumentscreate an output directory, then read in the data, and finally produce the plots.
 
