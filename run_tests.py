'''
This is the entry point to running all of your tests. 
You can do simple testing as we have done all year in your homework assignments. 
Or, you can leverage Python's Unit Test Framework which is a bit more complicated, but super cool.  

A common command to run the unit tests from the console is: python -m unittest discover -s tests -v

Your tests would all inherit from unittest.TestCase.

Take advantage of helper function in cse163_utils.py to help you with testing.
'''
import pandas as pd
from cse163_utils import assert_equals


def test_update_choropleth():
    '''
    This function just tests the correlation function from the interactive Plotly Dash app
    '''
    test_df = pd.DataFrame({
        "ISO_code": ["AUT", "AUT", "AUT", "BEL", "BEL", "BEL"],
        "fruit_intake_weekly": [1, 2, 3, 1, 2, 3],
        "tv_hours_weekdays": [1, 2, 3, 3, 2, 1]
    })

    # AUT: correlation = 1, BEL: correlation = -1
    # Because the original method dash_practice returns a figure,
    # I copied the code to test just the correlation and grouping here instead
    corr_df = test_df[["fruit_intake_weekly", "tv_hours_weekdays", "ISO_code"]].dropna()
    corr_df = corr_df.groupby('ISO_code') \
        .apply(lambda grp: grp["fruit_intake_weekly"].corr(grp["tv_hours_weekdays"]), include_groups=False) \
        .reset_index(name='correlation')
    assert_equals(received=corr_df.loc[corr_df["ISO_code"] == "AUT",
                  ["correlation"]].correlation.item(), expected=1.0)
    assert_equals(received=corr_df.loc[corr_df["ISO_code"] == "BEL",
                  ["correlation"]].correlation.item(), expected=-1.0)


if __name__ == "__main__":
    test_update_choropleth()