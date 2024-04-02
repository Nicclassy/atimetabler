from typing import Optional
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from constants import (
    UnitAssesment,
    UnitAssesments,

    SEMESTER_PATTERN,
    UNIT_URL_FORMAT,
    UNIT_NOT_FOUND_URL,

    TYPE,
    DESCRIPTION,
    WEIGHT,
    DUE,
    LENGTH,

    CHILDREN_XPATH,
    FIRST_TD_XPATH,
    ANCHOR_XPATH,

    UNIT_OFFERINGS_TABLE_XPATH,
    ASSESMENTS_TABLE_CHILDREN_XPATH,
    PRIMARY_XPATH,
    ASSESMENT_BUTTON_XPATH,
)

def _find_by_xpath(locator: WebElement | webdriver.Chrome, xpath: str) -> Optional[WebElement]:
    try:
        element = locator.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return None
    else:
        return element
    
def _get_semester(text: str) -> Optional[int]:
    if (semester_match := SEMESTER_PATTERN.match(text)) is not None:
        return int(semester_match.group(1))
    return None

def _get_unit_url(unit_code: str) -> str:
    return UNIT_URL_FORMAT.format(unit_code)

def _get_unit_outline_url(driver: webdriver.Chrome, target_semester: int) -> Optional[str]:
    unit_offerings_table = driver.find_element(By.XPATH, UNIT_OFFERINGS_TABLE_XPATH)
    for unit_offering in unit_offerings_table.find_elements(By.XPATH, CHILDREN_XPATH):
        semester = _get_semester(unit_offering.find_element(By.XPATH, FIRST_TD_XPATH).text)
        if semester == target_semester:
            unit_outline_element = _find_by_xpath(unit_offering, ANCHOR_XPATH)
            if unit_outline_element is not None:
                return unit_outline_element.get_attribute("href")
            else:
                return None
    else:
        return None

def _get_unit_assesment(tbody: WebElement) -> Optional[UnitAssesment]:
    if (row_parent := _find_by_xpath(tbody, PRIMARY_XPATH)) is None:
        return None
    row = row_parent.find_elements(By.XPATH, CHILDREN_XPATH)
    if len(row) != 5:
        return None

    return {
        TYPE: row[0].text,
        DESCRIPTION: row[1].text,
        WEIGHT: row[2].text,
        DUE: row[3].text,
        LENGTH: row[4].text
    }

def _get_unit_assesments(driver: webdriver.Chrome) -> UnitAssesments:
    assesment_button = driver.find_element(By.XPATH, ASSESMENT_BUTTON_XPATH)
    assesment_button.send_keys(Keys.RETURN)

    unit_assesments = []
    table_rows = driver.find_elements(
        By.XPATH, ASSESMENTS_TABLE_CHILDREN_XPATH
    )
    for row in table_rows:
        if (
            row.tag_name == "tbody" and 
            (unit_assesment := _get_unit_assesment(row)) is not None
        ):
            unit_assesments.append(unit_assesment)

    return unit_assesments

def _get_unit_assesments_in_semester(unit_code: str, 
                                     semester: int) -> Optional[UnitAssesments]:
    driver = webdriver.Chrome()
    unit_url = _get_unit_url(unit_code)
    driver.get(unit_url)

    if driver.current_url == UNIT_NOT_FOUND_URL:
        print("The page for", unit_code, "does not exist.")
        return None

    unit_outline_url = _get_unit_outline_url(driver, semester)
    if unit_outline_url is None:
        print("The unit outline for", unit_code, "in", semester, "was not found.")
        return None
    
    driver.get(unit_outline_url)

    unit_assesments = _get_unit_assesments(driver)
    driver.close()
    return unit_assesments

def get_assesments_for_units(unit_codes: list[str], 
                             semester: int) -> dict[str, UnitAssesments]:
    with ThreadPoolExecutor(max_workers=len(unit_codes)) as executor:
        futures = {
            unit_code: executor.submit(
                _get_unit_assesments_in_semester, 
                unit_code, semester
            ) 
            for unit_code in unit_codes
        }
        return {
            unit_code: future.result() 
            for unit_code, future in futures.items()
        }

