from selenium.webdriver.remote.webelement import WebElement

from constants import (
    UnitAssesment,

    TYPE,
    NAME,
    DESCRIPTION,
    WEIGHT,
    WEEK,
    DUE,
    LENGTH,
)

def _format_assesment_type(assesment_type: str) -> str:
    return assesment_type.split('\n')[0]

def _format_name_and_description(name_and_description: str) -> list[str, str]:
    return name_and_description.split('\n')

def _format_due_date_and_week(due_date_and_week: str) -> tuple[str, str]:
    dues = due_date_and_week.split('\n')
    if len(dues) == 2:
        week, due_date = dues
    else:
        week = None
        due_date = dues[0]

    if due_date == '-':
        due_date = None

    return week, due_date

def _format_length(length: str) -> str:
    if length == "n/a":
        length = None
    return length

def unit_assesment_from_web_elements(web_elements: list[WebElement]) -> UnitAssesment:
    assesment_type = _format_assesment_type(web_elements[0].text)
    name, description = _format_name_and_description(web_elements[1].text)
    weight = web_elements[2].text
    week, due_date = _format_due_date_and_week(web_elements[3].text)
    length = _format_length(web_elements[4].text)

    return {
        TYPE: assesment_type,
        NAME: name,
        DESCRIPTION: description,
        WEIGHT: weight,
        WEEK: week,
        DUE: due_date,
        LENGTH: length,
    }

