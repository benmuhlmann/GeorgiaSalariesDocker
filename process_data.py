"""
A script to process the georgia salaries made available on https://open.ga.gov/
with the eventual goal of creating a dashboard to visualize salary data
"""

import pandas as pd
import pickle

# Is it more efficient to parse all three names at once?

def get_last(name):
    """
    Get the state employee's last name
    :param name: the name as provided in the NAME field
    :return: the employee's last name
    """
    try:
        return name.split(',')[0].strip()
    except (IndexError, AttributeError):
        return 'Unknown'


def get_first(name):
    """
    Get the state employee's first name.
    :param name: the name as provided in the NAME field
    :return: the employee's first name
    """
    try:
        parts = name.split(',')[1].strip().split()
        return parts[0] if parts else 'Unknown'
    except (IndexError, AttributeError):
        return 'Unknown'


def get_middle(name):
    """
    Get the state employee's middle name or initial.
    If no middle name or initial, return empty string
    :param name: the name as provided in the NAME field
    :return: the employee's middle name or initial
    """
    try:
        parts = name.split(',')[1].strip().split()
        return parts[1] if len(parts) > 1 else ''
    except (IndexError, AttributeError):
        return ''


print("Loading dataset")
all_salaries = pd.read_csv('SalaryTravelDataExportAllYears.txt', 
                          encoding='latin-1',
                          quotechar="'",  # Fields are wrapped in single quotes
                          sep=',',  # Proper CSV with comma separator
                          engine='c')  # Use the faster C engine since format is standard

# Debug: Print column names and first few rows
print("\nColumn names:", all_salaries.columns.tolist())
print("\nSample names before processing:")
sample_names = all_salaries['NAME'].head(10).tolist()
for name in sample_names:
    print(f"Original: {name}")
    print(f"  Last: {get_last(name)}")
    print(f"  First: {get_first(name)}")
    print(f"  Middle: {get_middle(name)}")
    print("---")

print("Extracting names and formatting values")
all_salaries['FIRST_NAME'] = all_salaries['NAME'].apply(get_first)
all_salaries['MIDDLE_NAME'] = all_salaries['NAME'].apply(get_middle)
all_salaries['LAST_NAME'] = all_salaries['NAME'].apply(get_last)

# format name as first + last
# middle name parsing can be removed
all_salaries['NAME'] = (all_salaries['FIRST_NAME'].apply(str.capitalize)
                        + ' '
                        + all_salaries['LAST_NAME'].apply(str.capitalize))

# there are a few nan Titles, so fill those before changing values to title case
all_salaries['TITLE'] = (all_salaries['TITLE'].fillna('None')
                                              .apply(str.title))

# Reformat organization values as title-case
all_salaries['ORGANIZATION'] = all_salaries['ORGANIZATION'].apply(str.title)


#  sort dataframe by year so displayed
#  results table appears in chronological order
all_salaries = all_salaries.sort_values(by=['FISCAL_YEAR', 'SALARY'], ascending=[True, False])

# only keep columns relevant to dashboard
all_salaries = all_salaries[['NAME', 'TITLE', 'ORGANIZATION', 'SALARY', 'FISCAL_YEAR']]

# rename columns
all_salaries = all_salaries.rename(columns={'NAME': 'Name',
                                            'TITLE': 'Title',
                                            'ORGANIZATION': 'Organization',
                                            'SALARY': 'Salary',
                                            'FISCAL_YEAR': 'Fiscal Year'})

with open('all_salaries.pickle', 'wb') as file1:
    pickle.dump(all_salaries, file1)



