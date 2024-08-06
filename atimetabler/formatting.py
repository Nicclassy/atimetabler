from datetime import datetime
from typing import Optional
from selenium.webdriver.remote.webelement import WebElement

from atimetabler.constants import (
    UnitAssesment,

    DUE_DATE_TEXT_PATTERN,

    TYPE,
    NAME,
    DESCRIPTION,
    WEIGHT,
    WEEK,
    DUE,
    LENGTH,
)

DUE_DATE_FORMAT = "%d %b %Y at %H:%M"
NEW_DUE_DATE_FORMAT = "%B %d %Y at %I:%M%p"

def _format_assesment_type(assesment_type: str) -> str:
    return assesment_type.split('\n')[0]

def _format_name_and_description(name_and_description: str) -> Optional[list[str, Optional[str]]]:
    values = name_and_description.split('\n')
    if len(values) == 1:
        return [values[0], None]
    return values or None

def _format_due_date(due_date: Optional[str]) -> Optional[str]:
    if due_date is None:
        return due_date
    
    due_date = DUE_DATE_TEXT_PATTERN.sub('', due_date)
    try:
        dt = datetime.strptime(due_date, DUE_DATE_FORMAT)
        return dt.strftime(NEW_DUE_DATE_FORMAT).replace("AM", "am").replace("PM", "pm")
    except ValueError:
        return due_date
    
def _format_due_date_and_week(due_date_and_week: str) -> tuple[str, str]:
    dues = due_date_and_week.split('\n')
    if len(dues) >= 2:
        week, due_date = dues[:2]
    else:
        week = dues[0]
        due_date = None

    if due_date == '-':
        due_date = None
    if week == '-':
        week = None

    return week or None, _format_due_date(due_date)

def _format_length(length: str) -> str:
    if length.lower() == "n/a":
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

