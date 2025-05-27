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


def preprocess_dataset(file_name, json_name):
    '''
    This method keeps only relevant columns in the provided dataset
    and renames them to more understandable names
    '''
    rename_map = {}
    with open(json_name, 'r') as fp:
        rename_map = json.load(fp)
    df = pandas.read_csv("./raw_data/" + file_name)

    columns_to_keep = list(rename_map.keys())
    # Removes any columns not found in current years data
    for col in rename_map.keys():
        if col not in df.columns:
            columns_to_keep.remove(col)

    df_filtered = df[columns_to_keep].rename(columns=rename_map)

    # save this data to a new csv in the data_organized folder
    output_dir = './data_organized'
    output_file = os.path.join(output_dir, file_name)
    df_filtered.to_csv(output_file, index=False)


def main():
    # Uncomment line below ONLY if working with original, unzipped .sas7bdat files
    # nsch_to_csv()
    # for i in range(16, 24):
    #     preprocess_dataset("nsch_20" + str(i) + "e_topical.csv", "nsch_columns.json")
    # preprocess_dataset("HBSC2002.csv", "hbsc_columns.json")
    # preprocess_dataset("HBSC2006.csv", "hbsc_columns.json")
    # preprocess_dataset("HBSC2010.csv", "hbsc_columns.json")
    # preprocess_dataset("HBSC2014.csv", "hbsc_columns.json")
    preprocess_dataset("HBSC2018.csv", "hbsc_columns.json")

if __name__ == "__main__":
    main()