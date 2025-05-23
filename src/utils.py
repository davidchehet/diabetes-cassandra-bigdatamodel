"""
utils.py includes helper methods that are used across
all other python files.  
"""

def get_query_by_tag(filename, tag):
    """
    Navigate a CQL file, and using the tag,
    return CQL query to be ran. Meant to be 
    used to avoid direct queries in .py files.

    Args:
        filename: The path that contains CQL files
        tag: The comment above the query to use

    Returns:
        The string containing the query
    """
    with open(filename) as f:
        content = f.read()
    sections = content.split('-- [')
    for section in sections:
        if section.startswith(tag + ']'):
            return section.split(']', 1)[1].strip().rstrip(';')
    return None

def binarize_gender(gender):
    """
    Take in a string value ['Female', 'Male', 'Other'],
    return 0 if value is 'Female' or 'Other',
    return 1 if value is 'Male'.

    Args:
        gender: A passed in value from our bronze DB

    Returns:
        int
    """
    if gender == 'Female':
        return 0
    elif gender == 'Male':
        return 1
    
    # For gender 'Other'
    return 0

def format_location(location):
    """
    Take in a location string, strip white
    space, and put it into title case.

    Args:
        location: Original string of patient's tate

    Returns:
        Formatted string in title case
    """
    return location.strip().title()

def categorize_smoking_history(history):
    """
    Clean string value of smoking_history
    to a numerical mapping as follows:

    'never': 0
    'ever': 0 -> assume mispelling of 'never'
    'not current': 1
    'former': 1 -> synonymous with 'not current'
    'current': 2
    'No Info': -1 

    Args:
        history: string value of smoking history
    
    Returns:
        int in range [-1, 2]
    """
    if history == 'never' or history == 'ever':
        return 0
    elif history == 'not current' or history == 'former':
        return 1
    elif history == 'current':
        return 2
    
    # 'No Info'
    return -1

def check_health_condition(row):
    """
    Take in a row of data from a dataframe.
    Check if the patient has hypertension,
    heart disease, or both.

    Args:
        row: A row from a dataframe

    Returns:
        A string that classifies health condition
    """
    if row['hypertension'] == 1 and row['heart_disease'] == 1:
        return "Hypertension & Heart Disease"
    elif row['hypertension'] == 1:
        return "Hypertension Only"
    elif row['heart_disease'] == 1:
        return "Heart Disease Only"
    
    # Both columns have value of 0
    return "Neither"

def check_race(row):
    """
    Take in a row of data from a dataframe.
    Check what is the race of the patient.

    Args:
        row: A row from a dataframe

    Returns:
        A string that classifies patient race
    """
    if row['race_african_american'] == 1:
        return "African American"
    elif row['race_asian'] == 1:
        return "Asian"
    elif row['race_caucasian'] == 1:
        return "Caucasian"
    elif row['race_hispanic'] == 1:
        return "Hispanic"
    elif row['race_other'] == 1:
        return "Other"
    
    return None