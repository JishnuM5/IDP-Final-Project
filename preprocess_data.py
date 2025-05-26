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


def to_csv(file_name):
    '''
    This method takes any file path to a dataset and converts it to a .csv file
    '''
    df = pandas.read_sas(file_name)
    save_string = file_name[:file_name.index(".") + 1] + "csv"
    df.to_csv(save_string, index=False)


def preprocess_nsch():
    '''
    This method keeps only relevant columns in the NSCH dataset
    and renames them to more understandable names.
    '''

    # a list of all relevant columns we want to keep
    columns_to_keep = ["CBSAFP_YN", "FIPSST", "METRO_YN", "MPC_YN", "SC_AGE_LT10", "SC_AGE_LT4", "SC_AGE_LT6", "SC_AGE_LT9", "SC_AGE_YEARS", "SC_HISPANIC_R", "SC_RACE_R", "SC_SEX", "AGEPOS4", "TOTKIDS_R", "TOTCSHCN", "SC_CSHCN", "SC_K2Q11", "SC_K2Q13", "SC_K2Q14", "SC_K2Q16", "SC_K2Q19", "SC_K2Q22", "SC_K2Q23", "ADDTREAT", "ANYOTHER", "ANYOTHER_CURR", "ANYOTHER_DESC", "AUTISMMED", "AUTISMTREAT", "BULLIED", "BULLIED_R", "K7Q71_R", "BULLY", "DOWNSYN", "DOWNSYN_CURR", "DOWNSYN_DESC", "ERRANDALONE", "HCABILITY", "HCEXTENT", "HEADACHE", "HEADACHE_CURR", "HEADACHE_DESC", "K2Q01", "K2Q30A", "K2Q30B", "K2Q30C", "K2Q31A", "K2Q31B", "K2Q31C", "K2Q32A", "K2Q32B", "K2Q32C", "K2Q33A", "K2Q33B", "K2Q33C", "K2Q34A", "K2Q34B", "K2Q34C", "K2Q35A", "K2Q35A_1_YEARS", "K2Q35B", "K2Q35C", "K2Q35D", "K2Q36A", "K2Q36B", "K2Q36C", "K2Q46A", "K2Q46B", "K2Q46C", "K2Q60A", "K2Q60B", "K2Q60C", "K6Q70_R", "K6Q71_R", "K6Q72_R", "K6Q73_R", "K7Q70_R", "K7Q72_R", "K7Q73_R", "K7Q74_R", "K7Q75_R", "MEMORYCOND", "SUBABUSE", "SUBABUSE_CURR", "SUBABUSE_DESC", "K4Q22_R", "K4Q23", "K4Q28X04", "K4Q36", "K4Q37", "K4Q38", "K6Q10", "SESCURRSVC", "SESPLANYR", "TREATNEED", "WEIGHT", "K6Q15", "OVERWEIGHT", "MENBEVCOV", "STOPWORK", "CALMDOWN", "CALMDOWN_R", "DISTRACTED", "EXPULSION", "FOCUSON", "GRADES", "HARDWORK", "HURTSAD", "K7Q02R_R", "K7Q04R_R", "K7Q30", "K7Q31", "K7Q32", "K7Q33", "K7Q37", "K7Q38", "MAKEFRIEND", "NAMEEMOTIONS", "NEWACTIVITY", "PHYSACTIV", "PLAYWELL", "REPEATED", "SITSTILL", "STARTSCHOOL", "TEMPER", "TEMPER_R", "WAITFORTURN", "WORKTOFIN", "BEDTIME", "BORNUSA", "K8Q35", "FRUIT", "HOURSLEEP", "HOURSLEEP05", "K11Q43R", "K6Q60_R", "K6Q61_R", "K8Q21", "K8Q30", "K8Q31", "K8Q32", "K8Q34", "K8Q35", "LIVEUSA_MO", "LIVEUSA_YR", "OUTDOORSWKDAY", "OUTDOORSWKEND", "SCREENTIME", "K7Q91_R", "K7Q60_R", "SUGARDRINK", "VEGETABLES", "ACE1", "A1_MENTHEALTH", "A1_AGE", "A1_EMPLOYED", "A1_EMPLOYED_R", "A1_K11Q50_R", "A2_AGE", "A2_EMPLOYED", "A2_EMPLOYED_R", "A2_MENTHEALTH", "A2_K11Q50_R", "HHCOUNT", "FAMILY", "FAMILY_R"]

    # a dictionary of old column names with new prefered names
    rename_map = {
        
    }

    df = pandas.read_csv("./raw_data/nsch_2023e_topical.csv")

    # Double checks that all the columns to keep are actually in the dataset (no typoes, etc)
    missing_cols = [col for col in columns_to_keep if col not in df.columns]
    if missing_cols:
        print("Warning: These columns are missing from the dataset:")
        print(missing_cols)

    df_filtered = df[columns_to_keep].rename(columns=rename_map)

    # save this data to a new csv in the data_organized folder
    output_dir = './data_organized'
    output_file = os.path.join(output_dir, 'filtered_dataset.csv')
    df_filtered.to_csv(output_file, index=False)



def main():
    to_csv("raw_data/nsch_2023e_topical.sas7bdat")


if __name__ == "__main__":
    main()