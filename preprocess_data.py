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
    This method takes any file path to an SAS dataset and converts it to a .csv file
    '''
    df = pandas.read_sas(file_name)
    save_string = file_name[:file_name.index(".") + 1] + "csv"
    df.to_csv(save_string, index=False)


# This function was used to create the initial NSCH raw data .csv files
# It is not necessary to run every time
def nsch_to_csv():
    # to_csv("raw_data/nsch_2023e_topical.sas7bdat")
    # to_csv("raw_data/nsch_2022e_topical.sas7bdat")
    # to_csv("raw_data/nsch_2021e_topical.sas7bdat")
    # to_csv("raw_data/nsch_2020e_topical.sas7bdat")
    # to_csv("raw_data/nsch_2019e_topical.sas7bdat")
    to_csv("raw_data/nsch_2018e_topical.sas7bdat")
    # to_csv("raw_data/nsch_2017e_topical.sas7bdat")
    # to_csv("raw_data/nsch_2016e_topical.sas7bdat")

# def preprocess_nsch():
#     '''
#     This method keeps only relevant columns in the NSCH dataset
#     and renames them to more understandable names.
#     '''

#     # a list of all relevant columns we want to keep
#     columns_to_keep = ["CBSAFP_YN", "FIPSST", "METRO_YN", "MPC_YN", "SC_AGE_LT10", "SC_AGE_LT4", "SC_AGE_LT6", "SC_AGE_LT9", "SC_AGE_YEARS", "SC_HISPANIC_R", "SC_RACE_R", "SC_SEX", "AGEPOS4", "TOTKIDS_R", "TOTCSHCN", "SC_CSHCN", "SC_K2Q11", "SC_K2Q13", "SC_K2Q14", "SC_K2Q16", "SC_K2Q19", "SC_K2Q22", "SC_K2Q23", "ADDTREAT", "ANYOTHER", "ANYOTHER_CURR", "ANYOTHER_DESC", "AUTISMMED", "AUTISMTREAT", "BULLIED", "BULLIED_R", "K7Q71_R", "BULLY", "DOWNSYN", "DOWNSYN_CURR", "DOWNSYN_DESC", "ERRANDALONE", "HCABILITY", "HCEXTENT", "HEADACHE", "HEADACHE_CURR", "HEADACHE_DESC", "K2Q01", "K2Q30A", "K2Q30B", "K2Q30C", "K2Q31A", "K2Q31B", "K2Q31C", "K2Q32A", "K2Q32B", "K2Q32C", "K2Q33A", "K2Q33B", "K2Q33C", "K2Q34A", "K2Q34B", "K2Q34C", "K2Q35A", "K2Q35A_1_YEARS", "K2Q35B", "K2Q35C", "K2Q35D", "K2Q36A", "K2Q36B", "K2Q36C", "K2Q46A", "K2Q46B", "K2Q46C", "K2Q60A", "K2Q60B", "K2Q60C", "K6Q70_R", "K6Q71_R", "K6Q72_R", "K6Q73_R", "K7Q70_R", "K7Q82_R", "K7Q83_R", "K7Q84_R", "K7Q85_R", "MEMORYCOND", "SUBABUSE",
#                        "SUBABUSE_CURR", "SUBABUSE_DESC", "K4Q22_R", "K4Q23", "K4Q28X04", "K4Q36", "K4Q37", "K4Q38", "K6Q10", "SESCURRSVC", "SESPLANYR", "TREATNEED", "WEIGHT", "K6Q15", "OVERWEIGHT", "MENBEVCOV", "STOPWORK", "CALMDOWN", "CALMDOWN_R", "DISTRACTED", "EXPULSION", "FOCUSON", "GRADES", "HARDWORK", "HURTSAD", "K7Q02R_R", "K7Q04R_R", "K7Q30", "K7Q31", "K7Q32", "K7Q33", "K7Q37", "K7Q38", "MAKEFRIEND", "NAMEEMOTIONS", "PHYSACTIV", "PLAYWELL", "REPEATED", "SITSTILL", "STARTSCHOOL", "TEMPER", "TEMPER_R", "WAITFORTURN", "WORKTOFIN", "BEDTIME", "BORNUSA", "K8Q35", "FRUIT", "HOURSLEEP", "HOURSLEEP05", "K11Q43R", "K6Q60_R", "K6Q61_R", "K8Q21", "K8Q30", "K8Q31", "K8Q32", "K8Q34", "K8Q35", "LIVEUSA_MO", "LIVEUSA_YR", "OUTDOORSWKDAY", "OUTDOORSWKEND", "SCREENTIME", "K7Q91_R", "K7Q60_R", "SUGARDRINK", "VEGETABLES", "ACE1", "A1_MENTHEALTH", "A1_AGE", "A1_EMPLOYED", "A1_EMPLOYED_R", "A1_K11Q50_R", "A2_AGE", "A2_EMPLOYED", "A2_EMPLOYED_R", "A2_MENTHEALTH", "A2_K11Q50_R", "HHCOUNT", "FAMILY", "FAMILY_R"]

#     # a dictionary of old column names as keys and the new prefered names as values
#     rename_map = {
#         "CBSAFP_YN": "Is_CBSA",
#         "FIPSST": "State_FIPS",
#         "METRO_YN": "Is_Metro_Area",
#         "MPC_YN": "Is_Principal_City",
#         "SC_AGE_LT10": "Age_LT_10_Months",
#         "SC_AGE_LT4": "Age_LT_4_Months",
#         "SC_AGE_LT6": "Age_LT_6_Months",
#         "SC_AGE_LT9": "Age_LT_9_Months",
#         "SC_AGE_YEARS": "Child_Age_Years",
#         "SC_HISPANIC_R": "Is_Hispanic",
#         "SC_RACE_R": "Child_Race",
#         "SC_SEX": "Child_Sex",
#         "AGEPOS4": "Child_Birth_Order",
#         "TOTKIDS_R": "Total_Children_HH",
#         "TOTCSHCN": "Children_With_SHCN",
#         "SC_CSHCN": "Selected_Child_SHCN",
#         "SC_K2Q11": "Child_Medication_Needed",
#         "SC_K2Q13": "Needs_More_Medical_Care",
#         "SC_K2Q14": "Medical_Care_Condition",
#         "SC_K2Q16": "Limited_Ability",
#         "SC_K2Q19": "Receives_Special_Therapy",
#         "SC_K2Q22": "Needs_Behavioral_Treatment",
#         "SC_K2Q23": "Behavioral_Issue_12mo",
#         "ADDTREAT": "ADHD_Treatment",
#         "ANYOTHER": "Other_Mental_Condition",
#         "ANYOTHER_CURR": "Other_Mental_Condition_Current",
#         "ANYOTHER_DESC": "Other_Mental_Condition_Severity",
#         "AUTISMMED": "Autism_Medication_Current",
#         "AUTISMTREAT": "Autism_Treatment_Recent",
#         "BULLIED": "Is_Bullied",
#         "BULLIED_R": "Bullied_Frequency",
#         "K7Q71_R": "Bullies_Others",
#         "BULLY": "Bullying_Frequency",
#         "DOWNSYN": "Has_Down_Syndrome",
#         "DOWNSYN_CURR": "Down_Syndrome_Current",
#         "DOWNSYN_DESC": "Down_Syndrome_Severity",
#         "ERRANDALONE": "Difficulty_Errands_Alone",
#         "HCABILITY": "Health_Affects_Ability",
#         "HCEXTENT": "Health_Affects_Extent",
#         "HEADACHE": "Has_Headaches",
#         "HEADACHE_CURR": "Headaches_Current",
#         "HEADACHE_DESC": "Headache_Severity",
#         "K2Q01": "General_Health",
#         "K2Q30A": "Has_Learning_Disability",
#         "K2Q30B": "Learning_Disability_Current",
#         "K2Q30C": "Learning_Disability_Severity",
#         "K2Q31A": "Has_ADHD",
#         "K2Q31B": "ADHD_Current",
#         "K2Q31C": "ADHD_Severity",
#         "K2Q32A": "Has_Depression",
#         "K2Q32B": "Depression_Current",
#         "K2Q32C": "Depression_Severity",
#         "K2Q33A": "Has_Anxiety",
#         "K2Q33B": "Anxiety_Current",
#         "K2Q33C": "Anxiety_Severity",
#         "K2Q34A": "Has_Behavior_Problems",
#         "K2Q34B": "Behavior_Problems_Current",
#         "K2Q34C": "Behavior_Problems_Severity",
#         "K2Q35A": "Has_Autism",
#         "K2Q35A_1_YEARS": "Autism_Diagnosis_Age",
#         "K2Q35B": "Autism_Current",
#         "K2Q35C": "Autism_Severity",
#         "K2Q35D": "Autism_Doctor_Type",
#         "K2Q36A": "Has_Developmental_Delay",
#         "K2Q36B": "Developmental_Delay_Current",
#         "K2Q36C": "Developmental_Delay_Severity",
#         "K2Q46A": "Has_Brain_Injury",
#         "K2Q46B": "Brain_Injury_Current",
#         "K2Q46C": "Brain_Injury_Severity",
#         "K2Q60A": "Has_Intellectual_Disability",
#         "K2Q60B": "Intellectual_Disability_Current",
#         "K2Q60C": "Intellectual_Disability_Severity",
#         "K6Q70_R": "Is_Affectionate",
#         "K6Q71_R": "Shows_Interest_Curiosity",
#         "K6Q72_R": "Smiles_Laughs",
#         "K6Q73_R": "Bounces_Back",
#         "K7Q70_R": "Argues_Too_Much",
#         "K7Q82_R": "Cares_About_School",
#         "K7Q83_R": "Does_Homework",
#         "K7Q84_R": "Finishes_Tasks",
#         "K7Q85_R": "Stays_Calm_When_Challenged",
#         "MEMORYCOND": "Difficulty_Concentrating",
#         "SUBABUSE": "Has_Substance_Use_Disorder",
#         "SUBABUSE_CURR": "Substance_Use_Disorder_Current",
#         "SUBABUSE_DESC": "Substance_Use_Disorder_Severity",
#         "K4Q22_R": "Received_Mental_Health_Treatment",
#         "K4Q23": "Takes_Emotional_Behavior_Meds",
#         "K4Q28X04": "Unmet_Mental_Health_Need",
#         "K4Q36": "Received_Special_Services",
#         "K4Q37": "Special_Services_Age",
#         "K4Q38": "Special_Services_Current",
#         "K6Q10": "Asked_About_Dev_Behavior_Concerns",
#         "SESCURRSVC": "Special_Ed_Plan_Current",
#         "SESPLANYR": "Special_Ed_Start_Age",
#         "TREATNEED": "Needs_Mental_Health_Treatment_Problem",
#         "WEIGHT": "Child_Weight_KG",
#         "K6Q15": "Has_Special_Ed_Plan",
#         "OVERWEIGHT": "Doctor_Said_Overweight",
#         "MENBEVCOV": "Mental_Health_Insurance_Coverage",
#         "STOPWORK": "Family_Stopped_Work_For_Child_Health",
#         "CALMDOWN": "Can_Calm_Down_Quickly",
#         "CALMDOWN_R": "Trouble_Calming_Down",
#         "DISTRACTED": "Easily_Distracted",
#         "EXPULSION": "Asked_To_Stay_Home_Behavior",
#         "FOCUSON": "Can_Focus_On_Task",
#         "GRADES": "School_Grades",
#         "HARDWORK": "Keeps_Working_Through_Difficulty",
#         "HURTSAD": "Shows_Concern_For_Others",
#         "K7Q02R_R": "Days_Missed_School_Illness",
#         "K7Q04R_R": "School_Contact_Problems",
#         "K7Q30": "Sports_Participation_Past_Year",
#         "K7Q31": "Clubs_Or_Organizations_Participation",
#         "K7Q32": "Organized_Activities_Participation",
#         "K7Q33": "Attends_Events_Or_Activities",
#         "K7Q37": "Did_Community_Service",
#         "K7Q38": "Has_Paid_Work",
#         "MAKEFRIEND": "Difficulty_Making_Friends",
#         "NAMEEMOTIONS": "Recognizes_Emotions",
#         "PHYSACTIV": "Daily_Physical_Activity",
#         "PLAYWELL": "Plays_Well_With_Others",
#         "REPEATED": "Repeated_A_Grade",
#         "SITSTILL": "Can_Sit_Still",
#         "STARTSCHOOL": "Has_Started_School",
#         "TEMPER": "Loses_Control",
#         "TEMPER_R": "Loses_Temper",
#         "WAITFORTURN": "Waits_Turn_Patiently",
#         "WORKTOFIN": "Works_Until_Complete",
#         "BEDTIME": "Consistent_Bedtime",
#         "BORNUSA": "Born_In_USA",
#         "K8Q35": "Has_Emotional_Support",
#         "FRUIT": "Fruit_Intake_Per_Week",
#         "HOURSLEEP": "Avg_Sleep_Hours_Per_Week",
#         "HOURSLEEP05": "Avg_Sleep_Hours_Day",
#         "K11Q43R": "Times_Moved_House",
#         "K6Q60_R": "Days_Read_To_Child",
#         "K6Q61_R": "Days_Tell_Stories_To_Child",
#         "K8Q21": "Good_Communication_With_Child",
#         "K8Q30": "Handles_Parenting_Demands",
#         "K8Q31": "Feels_Child_Hard_To_Care_For",
#         "K8Q32": "Feels_Child_Bothers_Them",
#         "K8Q34": "Feels_Angry_At_Child",
#         "LIVEUSA_MO": "Months_Lived_In_US",
#         "LIVEUSA_YR": "Years_Lived_In_US",
#         "OUTDOORSWKDAY": "Outdoor_Play_Weekday",
#         "OUTDOORSWKEND": "Outdoor_Play_Weekend",
#         "SCREENTIME": "Screen_Time_Total",
#         "K7Q91_R": "Screen_Time_Computers",
#         "K7Q60_R": "Screen_Time_TV",
#         "SUGARDRINK": "Sugary_Drinks_Per_Week",
#         "VEGETABLES": "Vegetables_Per_Week",
#         "ACE1": "Struggles_With_Basics",
#         "A1_MENTHEALTH": "Adult1_Mental_Health",
#         "A1_AGE": "Adult1_Age",
#         "A1_EMPLOYED": "Adult1_Employment_Status",
#         "A1_EMPLOYED_R": "Adult1_Employment_Status_New",
#         "A1_K11Q50_R": "Adult1_Employed_50_Weeks",
#         "A2_AGE": "Adult2_Age",
#         "A2_EMPLOYED": "Adult2_Employment_Status",
#         "A2_EMPLOYED_R": "Adult2_Employment_Status_New",
#         "A2_MENTHEALTH": "Adult2_Mental_Health",
#         "A2_K11Q50_R": "Adult2_Employed_50_Weeks",
#         "HHCOUNT": "Household_Size",
#         "FAMILY": "Family_Structure",
#         "FAMILY_R": "Family_Structure_New"
#     }

#     df = pandas.read_csv("./raw_data/nsch_2023e_topical.csv")

#     # Double checks that all the columns to keep are actually in the dataset (no typoes, etc)
#     missing_cols = [col for col in columns_to_keep if col not in df.columns]
#     if missing_cols:
#         print("Warning: These columns are missing from the dataset:")
#         print(missing_cols)

#     df_filtered = df[columns_to_keep].rename(columns=rename_map)

#     # save this data to a new csv in the data_organized folder
#     output_dir = './data_organized'
#     output_file = os.path.join(output_dir, 'filtered_dataset.csv')
#     df_filtered.to_csv(output_file, index=False)


def main():
    # Uncomment line below ONLY if working with orignal, unzipped .sas7bdat files
    nsch_to_csv()

    # preprocess_nsch()


if __name__ == "__main__":
    main()