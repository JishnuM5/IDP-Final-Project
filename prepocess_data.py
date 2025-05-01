'''
This file is intended to do the following types of work:
    * download data from APIs  
    * screenscrape data from websites  
    * reduce the size of large datasets to something more manageable  
    * clean data: reduce/rename columns, normalize strings, adjust values  
    * generate data through relatively complicated calculations   
'''

import pandas


def to_csv(file_name):
    '''
    This method takes any file path to a dataset and converts it to a .csv file
    '''
    df = pandas.read_sas(file_name)
    save_string = file_name[:file_name.index(".") + 1] + "csv"
    df.to_csv(save_string, index=False)  


def main():
    to_csv("raw_data/nsch_2023e_topical.sas7bdat")


if __name__ == "__main__":
    main()  