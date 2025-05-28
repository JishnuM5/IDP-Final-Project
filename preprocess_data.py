'''
This file is intended to do the following types of work:
    * download data from APIs  
    * screenscrape data from websites  
    * reduce the size of large datasets to something more manageable  
    * clean data: reduce/rename columns, normalize strings, adjust values  
    * generate data through relatively complicated calculations   
'''

import os
import json
import pandas as pd
import math


def to_csv(file_name):
    '''
    This method takes any file path to an SAS dataset and converts it to a .csv file
    '''
    df = pd.read_sas(file_name)
    save_string = file_name[:file_name.index(".") + 1] + "csv"
    df.to_csv(save_string, index=False)


def nsch_to_csv():
    '''
    This function was used to create the initial NSCH raw data .csv files
    It is not necessary to run every time
    '''
    for i in range(16, 24):
        to_csv("nsch_20" + str(i) + "e_topical.csv")


def trim_rename_dataset(file_name, json_name, delimiter):
    '''
    This method keeps only relevant columns in the provided dataset
    and renames them to more understandable names.
    '''
    rename_map = {}
    with open(json_name, 'r') as fp:
        rename_map = json.load(fp)
    df = pd.read_csv("./raw_data/" + file_name, delimiter=delimiter)

    columns_to_keep = list(rename_map.keys())
    # Removes any columns not found in current years data
    for col in rename_map.keys():
        if col not in df.columns:
            columns_to_keep.remove(col)

    df_filtered = df[columns_to_keep].rename(columns=rename_map)
    return df_filtered


def preprocess_all():
    '''
    This method preprocesses all the datasets
    '''
    for i in range(16, 24):
        file_name = "nsch_20" + str(i) + "e_topical.csv"
        df = trim_rename_dataset(file_name, "nsch_columns.json", ",")
        preprocess_nsch_dataset(df, file_name)
    for i in range(2, 15, 4):
        file_name = f"HBSC20{i:02}.csv"
        df = trim_rename_dataset(file_name, "hbsc_columns.json", ",")
        preprocess_hbsc_dataset(df, file_name)

    # The 2018 file used semicolons as delimiters, so had to be done separately
    df = trim_rename_dataset("HBSC2018.csv", "hbsc_columns.json", ";")
    preprocess_hbsc_dataset(df, "HBSC2018.csv")


def preprocess_nsch_dataset(df, file_name):
    # Removes the b'' from the values (which is added by read_csv() during parsing)
    df["State_FIPS"] = df["State_FIPS"].apply(lambda str: str[2:len(str) - 1])

    # Creates screen time column in 2016 and 2017 datasets, removes NaN screen time values
    if ("2016" in file_name or "2017" in file_name):
        # The .copy() explicitly creates a copy to avoid returning a view in some cases
        df = df.dropna(subset=["Screen_Time_Computers", "Screen_Time_TV"], how="any").copy()
        df["Screen_Time_Total"] = df["Screen_Time_Computers"] + df["Screen_Time_TV"]
    else:
        df = df.dropna(subset=["Screen_Time_Total"]).copy()

    # Save this data to a new csv in the data_organized folder
    df.to_csv(os.path.join('./data_organized', file_name), index=False)


def preprocess_hbsc_dataset(df, file_name):
    country_map = {}
    with open("country_codes.json", 'r') as fp:
        country_map = json.load(fp)
    df["ISO_code"] = df["country_region"].apply(lambda num: country_map[str(num)])
    df = df.drop('country_region', axis=1)

    quant_maps = []
    with open("hbsc_quant_codes.json", 'r') as fp:
        quant_maps = json.load(fp)
    for map in quant_maps:
        for col_name in map["columns"]:
            if col_name in df.columns:
                df[col_name] = df[col_name].apply(
                    lambda val: val if math.isnan(val) else map["mapping"][str(int(val))])
    if "2014" in file_name:
        col_names = ["talk_to_friends_phone_internet_freq", "talk_to_friends_text_freq",
                     "talk_to_friends_email_freq", "talk_to_friends_social_media_freq"]
        for col_name in col_names:
            mask = df[col_name] == "specify"
            spec_col_name = f'{col_name[0:len(col_name)-4]}daily'
            df.loc[mask, col_name] = df.loc[mask, spec_col_name]
            df = df.drop(spec_col_name, axis=1)

    # Save this data to a new csv in the data_organized folder
    df.to_csv(os.path.join('./data_organized', file_name), index=False)


def main():
    # Uncomment line below ONLY if working with original, unzipped .sas7bdat files
    # data_to_csv()
    preprocess_all()


if __name__ == "__main__":
    main()