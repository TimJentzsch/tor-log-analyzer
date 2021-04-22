"""
Utility functions.
"""
from typing import Dict


def clean_dict(d: Dict) -> Dict:
    """
    Creates a copy of the dictionary with all 'None' values removed.
    """
    cleaned_dict = {}

    for key, value in dict(d).items():
        if value is not None:
            cleaned_dict[key] = value

    return cleaned_dict
