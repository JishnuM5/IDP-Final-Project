# Organized Data
All organized data is ready to use as-is in this folder. To regenerate these files, run the [preprocess_data.py](../preprocess_data.py) file.

## The Process
Due to working with very large data that  

1. Involved many categorical values that had to be quantified, or placeholder values/labels that had to be mapped/decoded, and  
2. Data collected in surveys across years, with headers, values, and/or formats that had to be standardized,  

The data organization process was rather tedious and much more time-consuming than expected.  
To get a proper idea of how we would approach our dataset, and the level of initial consistency across datasets, we initially started by creating codebooks (manually) of the datasets, only keeping columns we thought would be useful for our project. The manual work was necessary to determine which columns were important. Plus, documentation for the databases often came in PDFs or non-tabular format, from which extracting these details would have been very complex. Across the 15 or so datasets, we had hundreds of variables, as well as track which ones change/are added/removed across years, which subsets of data the variables applied to, and other details. You can see all this work in our [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1DPWDouWsU9OGqHJ91Kc4gXF8BxNi3xkfTjNGgJj9k10/edit?usp=sharing).
  
The next step was renaming the columns. This was to  

1. Standardize column names across years, and
2. Convert them to more readable formats
  
Again, new names were added to our [spreadsheet](https://docs.google.com/spreadsheets/d/1DPWDouWsU9OGqHJ91Kc4gXF8BxNi3xkfTjNGgJj9k10/edit?usp=sharing). Afterwards, we converted the list from the spreadsheet to JSON files ([hbsc_columns](../data_maps/hbsc_columns.json) and [nsch_columns](../data_maps/nsch_columns.json)). After this, further survey-specific preprocessing was conducted. Most notably, we mapped numerical country labels to ISO-alpha 3 codes using the [country_codes.json](../data_maps/country_codes.json) we created and we quantified many, many columns in the HBSC datasets using [hbsc_quant_codes.json](../data_maps/hbsc_quant_codes.json). The process for creating both these JSON from the documentation can generally be seen in the aforementioned Google Sheet.