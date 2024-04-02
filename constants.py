import os
import re

os.chdir(os.path.dirname(__file__))

UnitAssesment = dict[str, str]
UnitAssesments = list[UnitAssesment]

HEADLESS_BROWSER = True
ENABLE_CACHING = True
SEMESTER_PATTERN = re.compile(r"Semester (\d) \d+")

TYPE = "type"
NAME = "name"
DESCRIPTION = "description"
WEIGHT = "weight"
WEEK = "week"
DUE = "due"
LENGTH = "length"

UNIT_URL_FORMAT = "https://www.sydney.edu.au/units/{}"
UNIT_NOT_FOUND_URL = "https://www.sydney.edu.au/errors/500.html"

FIRST_ELEMENT_XPATH = './*[1]'
CHILDREN_XPATH = './*'
FIRST_TD_XPATH = './td'
ANCHOR_XPATH = './td/a'

UNIT_OFFERINGS_TABLE_XPATH = '//*[@id="current-year"]/tbody'
ASSESMENTS_TABLE_CHILDREN_XPATH = '//*[@id="assessment-table"]/*'
PRIMARY_XPATH = ".//tr[@class='primary']"
ASSESMENT_BUTTON_XPATH = '//a[@title="Assessment details"]'