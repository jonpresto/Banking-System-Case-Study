#!/usr/bin/env python

"""
@Author: Jonathan Presto
@Date: 2022-06-20

This file serves as a set of utility functions to validate
a date string and credit card number used in the Bank Model.
The file should be imported to the file "bank_classes_and_io_funcs.py"

"""

import datetime
import csv
import pprint as pp
import pandas as pd
import re
import logging
from dateutil.relativedelta import relativedelta


# set-up logger main
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

fileHandler = logging.FileHandler('main.log')
fileHandler.setLevel(logging.INFO)
format = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
fileHandler.setFormatter(format)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)


# check for valid credit card
pattern1 = "^[456][0-9]{3}-?[0-9]{4}-?[0-9]{4}-?[0-9]{4}$"
pattern2 = r"((\d)(?!\2{3})){16}"

def is_valid_card_number(sequence):
    """Returns True if the sequence is a valid credit card number.

    A valid credit card number
    - must contain exactly 16 digits,
    - must start with a 4, 5 or 6 
    - must only consist of digits (0-9) or hyphens '-',
    - may have digits in groups of 4, separated by zero or one hyphen "-". 
    - must NOT use any other separator like ' ' , '_',
    - must NOT have 4 or more consecutive repeated digits.
    """

    if re.match(pattern1,sequence) == None:
        return False
    
    sequence = sequence.replace("-", "")
    if re.match(pattern2, sequence) == None:
        return False
    
    return True
    

# check for valid date string
PATTERN = '^\d{4}-\d{2}-\d{2}$'

def is_valid_date(sequence):
    """Returns True if the sequence is a valid string format YYYY-MM-DD.
    Year must be at least 1900.
    Month must be between 1 and 12 after casting datepart to int.
    Day must be between 12 and 31 after casting datepart to int.
    """
 
    #parse date parts to further validate range
    try:
        yyyy,mm,dd = sequence.split('-')
    except ValueError:
        return False
    
    match = re.match(PATTERN,sequence)
      
    if match == None:
        return False
    elif (int(mm) < 1 or int(mm) > 12):
        return False
    elif (int(dd) < 1 or int(dd) > 31):
        return False
    elif (int(yyyy) < 1900):
        return False

    return True
    
### EOF