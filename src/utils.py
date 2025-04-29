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