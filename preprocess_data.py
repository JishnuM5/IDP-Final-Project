'''
This file is intended to do the following types of work:
    * download data from APIs  
    * screenscrape data from websites  
    * reduce the size of large datasets to something more manageable  
    * clean data: reduce/rename columns, normalize strings, adjust values  
    * generate data through relatively complicated calculations   
'''

import pandas
import os
import json


def to_csv(file_name):
    '''
    This method takes any file path to an SAS dataset and converts it to a .csv file
    '''
    df = pandas.read_sas(file_name)
    save_string = file_name[:file_name.index(".") + 1] + "csv"
    df.to_csv(save_string, index=False)


def nsch_to_csv():
    '''
    This function was used to create the initial NSCH raw data .csv files
    It is not necessary to run every time
    '''
    to_csv("raw_data/nsch_2023e_topical.sas7bdat")
    to_csv("raw_data/nsch_2022e_topical.sas7bdat")
    to_csv("raw_data/nsch_2021e_topical.sas7bdat")
    to_csv("raw_data/nsch_2020e_topical.sas7bdat")
    to_csv("raw_data/nsch_2019e_topical.sas7bdat")
    to_csv("raw_data/nsch_2018e_topical.sas7bdat")
    to_csv("raw_data/nsch_2017e_topical.sas7bdat")
    to_csv("raw_data/nsch_2016e_topical.sas7bdat")


def preprocess_nsch():
    '''
    This method keeps only relevant columns in the NSCH dataset
    and renames them to more understandable names.
    '''
    # A dictionary of column names to keep and new, more readable column names
    # The dictionary is stored in a JSON file for cleanliness
    rename_map = {}
    with open('rename.json', 'r') as fp:
        rename_map = json.load(fp)

    df = pandas.read_csv("./raw_data/nsch_2023e_topical.csv")

    # Double checks that all the columns to keep are actually in the dataset (no typos, etc)
    missing_cols = [col for col in rename_map.keys() if col not in df.columns]
    if missing_cols:
        print("Warning: These columns are missing from the dataset:")
        print(missing_cols)

    df_filtered = df[rename_map.keys()].rename(columns=rename_map)

    # save this data to a new csv in the data_organized folder
    output_dir = './data_organized'
    output_file = os.path.join(output_dir, 'filtered_dataset.csv')
    df_filtered.to_csv(output_file, index=False)


def main():
    # Uncomment line below ONLY if working with original, unzipped .sas7bdat files
    # nsch_to_csv()

    preprocess_nsch()


if __name__ == "__main__":
    main()