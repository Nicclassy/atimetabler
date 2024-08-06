import os
import re

os.chdir(os.path.dirname(__file__))

UnitAssesment = dict[str, str]
UnitAssesments = list[UnitAssesment]

HEADLESS_BROWSER = False
ENABLE_CACHING = True

SEMESTER_PATTERN = re.compile(r"Semester (\d) \d+")
DUE_DATE_TEXT_PATTERN = re.compile("^Due date: ")

SEMESTER = 1
TYPE = "type"
NAME = "name"
DESCRIPTION = "description"
WEIGHT = "weight"
WEEK = "week"
DUE = "due"
LENGTH = "length"
CSV_FIELD_NAMES = (TYPE, NAME, DESCRIPTION, WEIGHT, WEEK, DUE, LENGTH)

UNIT_URL_FORMAT = "https://www.sydney.edu.au/units/{}"
UNIT_500_ERROR_URL = "https://www.sydney.edu.au/errors/500.html"
UNIT_404_ERROR_URL = "https://www.sydney.edu.au/errors/uosoutline-404.html"
UNIT_ERROR_URLS = {UNIT_500_ERROR_URL, UNIT_404_ERROR_URL}

FIRST_ELEMENT_XPATH = './*[1]'
CHILDREN_XPATH = './*'
FIRST_TD_XPATH = './td'
ANCHOR_XPATH = './td/a'

UNIT_OFFERINGS_TABLE_XPATH = '//*[@id="current-year"]/tbody'
ASSESMENTS_TABLE_CHILDREN_XPATH = '//*[@id="assessment-table"]/*'
PRIMARY_XPATH = ".//tr[@class='primary']"
ASSESMENT_BUTTON_XPATH = '//a[@title="Assessment details"]'
