# Ryan Neilson 1/13/26

# This will be a python script to automate the generation of samplesheets

#TODO
# Test with various conditions:
# User will input a sample sheet, need to add in the column name (which is harcoded as Sample right now).
# Right now the samplesheet sample column has to match part of the fastq string...not sure if this is always the case. 


# Import required libraries 

import os, sys # os lib for file/directory management 

import csv # csv lib to read/write csv

import argparse

import pandas as pd 


# Function 1: Nfcore-RNAseq, Read directory containing files to put into samplesheet

def read_raw_reads_directory(raw_read_dir):

    # Function: This will read the directory containing all of the raw reads

    # Parameters: raw_read_dir = the directory containg the raw reads

    # Save the fastq file names to var 

    raw_reads_list = os.listdir(raw_read_dir) # Saves a list of the fastq files in user directory 

    return raw_reads_list


def read_sample_submission_sheet(sample_sheet):

    # Read in the excel sheet
    # Create a pandas df 

    sample_sub_df = pd.read_csv(sample_sheet)

    sample_sub_df['Sample'] = sample_sub_df['Sample'].str.strip() # This will remove all trailing whitespace

    return sample_sub_df # Returns a pandas df, can use the Sample column to access the sample names


# Function 3: Nfcore-RNAseq, Write csv file to generate the samplesheet 

def write_samplesheet_to_output(output_dir, sample_sub_df, raw_reads_list):

    # Function: This will write the csv to the user output directory

    # Params: 
    # 1) output_dir: User defined dir to write the csv 
    # 2) raw_reads_list: The list of the fastq files 

    # Column names for nfcore/rnaseq pipeline
    # This is for paired_end only

    # Open file using the full path given by the user for the output directory

    rnaseq_samplesheet_name = "samplesheet.csv"

    csv_full_path = os.path.join(output_dir, rnaseq_samplesheet_name) # This will join the output directory and samplesheet name as a file path

    rnaseq_col_names = ['sample', 'fastq_1', 'fastq_2', 'strandedness']

    with open(csv_full_path, 'a', newline = '') as rnaseq_csvfile:
        #if os.stat(rnaseq_csvfile).st_size == 0: # Adds column name only when file is empty
        writer = csv.writer(rnaseq_csvfile)
        writer.writerow(rnaseq_col_names)
    
    # The header required by the nfcore/rnaseq samplesheet has been written

    rnaseq_csvfile.close

    # Parse each value of sample_sub_df
    # For sample ID in sample_sub_df sample column
        # if sample ID is equal to substring of fastq
        # append the sample id to rnaseq_samplesheet, fastq that matches, fastq below that matches and is R2, auto


    for sample_id in sample_sub_df["Sample"]:
        # sample_id is a string, and is the string to look for in each fastq name

        list_to_append = [] # this will a list containing the values to append to the samplesheet.csv

        # first, append the sample_id
        list_to_append.append(sample_id)

        for fastq_index in range(len(raw_reads_list)):
            if sample_id in raw_reads_list[fastq_index] and 'R1' in raw_reads_list[fastq_index]: # Makes sure R1 is appened first
                list_to_append.append(raw_reads_list[fastq_index]) # The raw_reads_list[fastq_index] is the fastq to append to csv
            
        for fastq_index in range(len(raw_reads_list)):
            if sample_id in raw_reads_list[fastq_index] and 'R2' in raw_reads_list[fastq_index]:
                list_to_append.append(raw_reads_list[fastq_index]) # The raw_reads_list[fastq_index] is the fastq to append to csv

        list_to_append.append('auto') # This will append auto to the end of the list

        # append the list_to_append to the next line of samplesheet
    
        with open(csv_full_path, 'a', newline = '') as rnaseq_csvfile:
        #if os.stat(rnaseq_csvfile).st_size == 0: # Adds column name only when file is empty
            writer = csv.writer(rnaseq_csvfile)
            writer.writerow(list_to_append) # this should write the list_to_append to the samplesheet


def main(argv):
# Main Function: Handle command line arguments utilized to build the samplesheet 

    # Insert note once debugging 
    parser = argparse.ArgumentParser()

    #parser.add_argument("--pipeline", type = str) # Provide users ability to choose which pipeline to make samplesheet for 
    parser.add_argument("--sample_directory", type = str) # Location of the directory containing all samplesheets
    parser.add_argument("--sample_sheet_directory", type = str) # Where the sample sheet is located
    parser.add_argument("--output_directory", type = str) # Where to store the csv 

    # Add user entered arguments as variable to utilize in functions 
    
    args = parser.parse_args()
    # Uncomment below once testing is done 
    raw_read_dir = args.sample_directory
    output_dir = args.output_directory
    sample_sheet = args.sample_sheet_directory

    #raw_read_dir = "/home/rneilson/VSCode/Scripts/nf_core_related/samplesheet_generator/raw_reads_test" # For testing

    #output_dir = "/home/rneilson/VSCode/Scripts/nf_core_related/samplesheet_generator/output_test" # For testing

    #sample_sheet = "/home/rneilson/VSCode/Scripts/nf_core_related/samplesheet_generator/sample_submission_sheet/sample_sub_test.csv" # For testing

    # Initialize each function

    raw_reads_list = read_raw_reads_directory(raw_read_dir)

    sample_sub_df = read_sample_submission_sheet(sample_sheet)

    write_samplesheet_to_output(output_dir, sample_sub_df, raw_reads_list)


if __name__ == '__main__':
    main(sys.argv)