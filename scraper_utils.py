from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from datetime import datetime, timedelta
import pandas as pd
import time


def clear_and_type_input(input_box, value):
    input_box.click()
    time.sleep(0.3)
    input_box.send_keys(Keys.CONTROL + "a")
    input_box.send_keys(Keys.DELETE)
    input_box.send_keys(Keys.CONTROL + "a")
    input_box.send_keys(Keys.DELETE)
    time.sleep(0.3)
    input_box.send_keys(value)
    time.sleep(0.7)
    # input_box.send_keys(Keys.ARROW_DOWN)  # trigger dropdown if needed



def get_dates(start_date_str, end_date_str):
    date_list = []

    # Convert strings to datetime objects using the format "dd/mm/yyyy"
    start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
    end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

    # Generate and print dates in the desired format
    current_date = start_date
    while current_date <= end_date:
        # Format the date as "dd/mm/yyyy" with leading zero in the month
        formatted_date = current_date.strftime("%d/%m/%Y")
        # print(formatted_date)
        date_list.append(formatted_date)
        current_date += timedelta(days=1)

    return date_list




def wait_for_backdrop_to_clear(driver, wait, timeout=10):
    try:
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiBackdrop-root")))
        print("Backdrop dismissed.")
    except:
        print(" Backdrop still visible after timeout — continuing anyway.")





def set_sending_country(driver, wait, country_name):
    try:
        # Locate input by index or context (adjust index as needed)
        inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
        print(inputs)
        sending_country_input = inputs[1]  # Assuming index 1 = Sending Country
        time.sleep(3)

        print('step 1')

        for attempt in range(2):  # Try max twice
            sending_country_input.click()
            time.sleep(1.2)
            sending_country_input.send_keys(Keys.CONTROL + "a")
            sending_country_input.send_keys(Keys.DELETE)
            sending_country_input.send_keys(Keys.CONTROL + "a")
            sending_country_input.send_keys(Keys.DELETE)
            sending_country_input.send_keys(Keys.CONTROL + "a")
            sending_country_input.send_keys(Keys.DELETE)
            time.sleep(1)
            sending_country_input.send_keys(country_name)
            time.sleep(0.5)

            try:

                dropdown_option = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//li[normalize-space()='{country_name}']"))
                )

                dropdown_option.click()
                print(f" Sending country set to: {country_name}")
                return
            except TimeoutException:
                print(f"Retrying dropdown for {country_name} (attempt {attempt + 1})")

        raise Exception(f"Could not select sending country: {country_name}")

    except Exception as e:
        print(f"Failed to set sending country: {e}")



def ensure_sending_country(driver, wait, expected_country="United Kingdom"):
    try:
        # Find all text inputs (you've seen it's usually at index 1)
        inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
        sending_input = inputs[1]

        # Get the current value
        actual_country = sending_input.get_attribute("value")

        if actual_country.strip().lower() == expected_country.lower():
            print(f"Confirmed sending country is '{actual_country}'")
            return True
        else:
            raise Exception(f"Sending country is '{actual_country}', expected '{expected_country}'")

    except Exception as e:
        print(f"[ERROR] Could not confirm sending country: {e}")
        raise


def select_receiving_country(driver, wait, country_name):
    try:
        # Locate input by index or context (adjust index as needed)
        inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
        print(inputs)
        sending_country_input = inputs[2]  # Assuming index 1 = Sending Country
        time.sleep(3)

        print('step 1')

        for attempt in range(2):  # Try max twice
            sending_country_input.click()
            time.sleep(1.2)
            sending_country_input.send_keys(Keys.CONTROL + "a")
            sending_country_input.send_keys(Keys.DELETE)
            sending_country_input.send_keys(Keys.CONTROL + "a")
            sending_country_input.send_keys(Keys.DELETE)

            time.sleep(1)
            sending_country_input.send_keys(country_name)
            time.sleep(0.5)

            try:

                dropdown_option = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//li[normalize-space()='{country_name}']"))
                )

                dropdown_option.click()
                print(f" Sending country set to: {country_name}")
                return
            except TimeoutException:
                print(f"Retrying dropdown for {country_name} (attempt {attempt + 1})")

        raise Exception(f"Could not select sending country: {country_name}")

    except Exception as e:
        print(f"Failed to set sending country: {e}")





# def select_receiving_country(driver, country_name):
#     try:
#         # Step 1: Locate input
#         inputs = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']"))
#         )
#         input_box = inputs[2]  # Receiving country field
#
#         # Step 2: Clear and type
#         clear_and_type_input(input_box, country_name)
#
#
#         # Step 3: Wait for dropdown to show up
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'MuiList-root')]"))
#         )
#
#         # Step 4: Find and click the closest match
#         options = driver.find_elements(By.XPATH, "//li[contains(@class, 'MuiAutocomplete-option')]")
#         for opt in options:
#             if country_name.lower() in opt.text.lower():
#                 label = opt.text  # Save the text BEFORE clicking
#                 opt.click()
#                 print(f"Selected receiving country: {label}")
#                 return
#
#         raise Exception(f" No matching dropdown option found for: {country_name}")
#
#     except TimeoutException:
#         print(f" Timeout: Dropdown never loaded for receiving country '{country_name}'")
#         raise
#
#     except Exception as e:
#         print(f"Failed to set receiving country '{country_name}': {e}")
#         raise
#




def ensure_receiving_country(driver, wait, expected_country):
    try:
        # Locate all input fields; receiving country is typically index 2
        inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
        receiving_input = inputs[2]

        # Read the value
        actual_country = receiving_input.get_attribute("value")

        if actual_country.strip().lower() == expected_country.lower():
            print(f"Confirmed receiving country is '{actual_country}'")
            return True
        else:
            raise Exception(f"Receiving country is '{actual_country}', expected '{expected_country}'")

    except Exception as e:
        print(f"[ERROR] Could not confirm receiving country: {e}")
        raise



from selenium.common.exceptions import TimeoutException















def select_all_options_in_dropdown(driver, wait, dropdown_aria_label):
    try:
        print(f"Opening dropdown: {dropdown_aria_label}")

        # Step 1: Click dropdown to open it
        dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//div[@role='combobox' and @aria-label='{dropdown_aria_label}']")))
        dropdown.click()
        time.sleep(1)

        # Step 2: Wait for dropdown list to appear
        wait.until(EC.presence_of_element_located((
            By.XPATH, "//ul[contains(@class, 'MuiList-root')]"
        )))

        # Step 3: Select all unchecked options
        options = driver.find_elements(By.XPATH, "//li[contains(@class, 'MuiButtonBase-root')]")
        actions = ActionChains(driver)

        for option in options:
            try:
                aria_selected = option.get_attribute("aria-selected")
                if aria_selected != "true":
                    # Scroll to the element
                    driver.execute_script("arguments[0].scrollIntoView(true);", option)
                    actions.move_to_element(option).perform()
                    time.sleep(0.1)

                    option.click()
                    time.sleep(0.3)
            except Exception as e:
                print(f" Warning clicking option: {e}")

        # Step 4: Click neutral content (like the table or main panel)
        try:
            content_area = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[contains(@class, 'MuiPaper-root') and not(contains(@class,'MuiPopover-paper'))]"
            )))
            actions.move_to_element(content_area).click().perform()
            time.sleep(0.5)
            print(" Clicked content area to close dropdown.")
        except Exception as e:
            print(f" Couldn't click content area: {e}")

        # Step 5: Wait for any remaining backdrop to go away
        try:
            wait.until(EC.invisibility_of_element_located(
                (By.CLASS_NAME, "MuiBackdrop-root")
            ))
        except:
            print("Backdrop may still be visible.")

        print(f"Finished selecting all in: {dropdown_aria_label}")

    except Exception as e:
        print(f" Failed to open or process dropdown '{dropdown_aria_label}': {e}")


def set_report_date(driver, wait, date_str):
    try:
        print(f"Setting report date to: {date_str}")

        # Step 1: Locate all text inputs
        inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))

        # Step 2: Assume first input is the date field
        date_input = inputs[0]

        # Step 3: Click and clear
        date_input.click()
        date_input.send_keys(Keys.CONTROL + "a")
        time.sleep(0.3)
        date_input.send_keys(Keys.DELETE)
        time.sleep(0.3)

        # Step 4: Type the new date
        date_input.send_keys(date_str)
        time.sleep(1)

        # Step 5: Press enter to dismiss calendar if open
        date_input.send_keys(Keys.ENTER)
        print("Date updated.")

        # Step 6: Click neutral content area to dismiss any overlay
        try:
            content_area = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[contains(@class, 'MuiPaper-root') and not(contains(@class,'MuiPopover-paper'))]"
            )))
            actions = ActionChains(driver)
            actions.move_to_element(content_area).click().perform()
            time.sleep(0.5)
            print("Clicked content area to close overlay.")
        except Exception as e:
            print(f"Couldn't click content area: {e}")

        # Step 7: Wait for any backdrop to disappear
        try:
            wait.until(EC.invisibility_of_element_located(
                (By.CLASS_NAME, "MuiBackdrop-root")
            ))
        except:
            print("Backdrop may still be visible.")

    except Exception as e:
        print(f"Failed to set report date: {e}")


def select_all_options_in_transfer_amount(driver, wait, dropdown_aria_label):
    try:
        print(f"Opening dropdown: {dropdown_aria_label}")

        # Step 1: Click dropdown to open it
        dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//div[@role='combobox' and @aria-label='{dropdown_aria_label}']")))
        dropdown.click()
        time.sleep(1)

        # Step 2: Wait for dropdown list to appear
        wait.until(EC.presence_of_element_located((
            By.XPATH, "//ul[contains(@class, 'MuiList-root')]"
        )))

        # Step 3: Select all unchecked options
        options = driver.find_elements(By.XPATH, "//li[contains(@class, 'MuiButtonBase-root')]")
        actions = ActionChains(driver)

        for option in options:
            try:
                aria_selected = option.get_attribute("aria-selected")
                if aria_selected != "true":
                    # Scroll to the element
                    driver.execute_script("arguments[0].scrollIntoView(true);", option)
                    actions.move_to_element(option).perform()
                    time.sleep(0.1)

                    option.click()
                    time.sleep(0.3)
            except Exception as e:
                print(f" Warning clicking option: {e}")

        # Step 4: Click neutral content
        try:
            content_area = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[contains(@class, 'MuiPaper-root') and not(contains(@class,'MuiPopover-paper'))]"
            )))
            actions.move_to_element(content_area).click().perform()
            time.sleep(0.5)
            print(" Clicked content area to close dropdown.")
        except Exception as e:
            print(f" Couldn't click content area: {e}")

        # Step 5: Wait for any remaining backdrop to go away
        try:
            wait.until(EC.invisibility_of_element_located(
                (By.CLASS_NAME, "MuiBackdrop-root")
            ))
        except:
            print("Backdrop may still be visible.")

        print(f"Finished selecting all in: {dropdown_aria_label}")

    except Exception as e:
        print(f" Failed to open or process dropdown '{dropdown_aria_label}': {e}")






def select_all_provider_checkboxes(driver):
    try:
        print("Selecting all provider checkboxes...")

        checkbox_selector = "input.PrivateSwitchBase-input"
        checkboxes = driver.find_elements(By.CSS_SELECTOR, checkbox_selector)

        for i in range(len(checkboxes)):
            try:
                # Re-fetch each checkbox before interacting
                checkbox = driver.find_elements(By.CSS_SELECTOR, checkbox_selector)[i]
                if not checkbox.is_selected():
                    checkbox.click()
                    time.sleep(0.1)
            except Exception as e:
                print(f"Skipped one checkbox due to stale reference: {e}")

        print("All available provider checkboxes selected.")

    except Exception as e:
        print(f"Failed to select provider checkboxes: {e}")





def click_download_report(driver, wait):
    try:
        print("Clicking 'Download Report'...")

        download_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(., 'Download Report')]"
        )))

        download_button.click()
        print( "Download button clicked.")

        time.sleep(5)

    except Exception as e:
        print(f"Failed to click 'Download Report': {e}")




def login_to_fxc(driver, wait):
    EMAIL = "ryanwh@remitly.com"
    PASSWORD = "ChargerPhone19!"

    driver.get("https://portal.fxcintel.com/analytics/dashboards/daily-table")
    wait.until(EC.url_contains("auth.fxcintel.com"))

    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_input = driver.find_element(By.ID, "password")

    username_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)

    sign_in_button = driver.find_element(By.XPATH, "//input[@type='submit']")
    sign_in_button.click()
