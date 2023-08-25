import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
 
class WebDriverFactory:
    @staticmethod
    def create_driver(driver_path, options):
        service = ChromeService(executable_path=driver_path)
        return webdriver.Chrome(service=service, options=options)

class IndexPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.niftyindices.com/reports/historical-data"

    def open(self):
        self.driver.get(self.url)
        time.sleep(10)  # Wait for the page to load
    def select_total_returns_index(self):
        # Locate the dropdown menu
        dropdown = self.driver.find_element(By.ID, 'HistoricalMenu')
        
        # Click the dropdown to open it
        dropdown.click()
        
        # Wait until the option is clickable
        wait = WebDriverWait(self.driver, 10)
        option_xpath = '//*[@id="mCSB_1_container"]/li[4]'
        option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        # Scroll to the option to ensure it's in view
        
        option.click()
        time.sleep(10)

    def select_equity_return_type(self):
        # Locate the dropdown menu for return type
        return_type_dropdown = self.driver.find_element(By.ID, 'ddlHistoricalreturntypee')
        # Scroll halfway down the page to ensure the dropdown is in view
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
        # Click the dropdown to open it
        return_type_dropdown.click()
        # Wait until the option is clickable
        wait = WebDriverWait(self.driver, 10)
        option_xpath2 = '//*[@id="ddlHistoricalreturntypee"]/option[3]'
        option2 = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath2)))
        option2.click()
        # Click outside the datepicker to close it
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.click()
        # Scroll into view if needed
        self.driver.execute_script("arguments[0].scrollIntoView();", option2)
        #Add a longer sleep time if needed
        time.sleep(5)  # Adjust the sleep time as needed

    def select_equity_tri(self, index_value):
        print("Selecting index type:")

        max_click_attempts = 10
        for _ in range(max_click_attempts):
            # Click on the dropdown menu to open it
            return_type_dropdown = self.driver.find_element(By.ID, 'ddlHistoricalreturntypeeindex')
            return_type_dropdown.click()

            # Select the option with the provided index value
            option = self.driver.find_element(By.XPATH, f'//*[@id="ddlHistoricalreturntypeeindex"]/option[{index_value}]')
            option.click()

            # Add a longer sleep time if needed
            time.sleep(5)  # Adjust the sleep time as needed
            print("Index selected successfully")

            # Print the selected value for verification
            selected_option = self.driver.execute_script('return document.querySelector("#ddlHistoricalreturntypeeindex").value;')
            print("Selected value:", selected_option)
            break  # Exit the loop if successful
        else:
            print("Dropdown did not open after multiple attempts")




              
    #function for start date selection


    def choose_start_date(self, year, month, row, col):
        print("Choosing start date:")

        # Click on the datepicker to open the calendar
        datepicker = self.driver.find_element(By.ID, 'datepickerFromtotalindex')
        datepicker.click()
        print("Datepicker opened")

        # Wait for the year dropdown to be clickable
        year_dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[2]')))
        year_dropdown.click()
        print("Year dropdown clicked")

        # Select the year using XPath
        year_option = self.driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/div/div/select[2]/option[text()="{year}"]')
        year_option.click()
        print(f"Selected year: {year}")

        # Wait for the month dropdown to be clickable
        month_dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]')))
        month_dropdown.click()
        print("Month dropdown clicked")

        # Select the month using XPath
        month_option = self.driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/div/div/select[1]/option[{month}]')
        month_option.click()
        print(f"Selected month: {month}")


        # Select the day
        day_element = self.driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[{row}]/td[{col}]/a')
        day_element.click()
        print(f"Selected day: Row {row}, Column {col}")

        # Click outside the datepicker to close it
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.click()
        print("Datepicker closed")


if __name__ == "__main__":
    driver_path = "/home/mohan/Documents/sample_webscrapper/chromedriver-linux64/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('--head')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver_factory = WebDriverFactory()
    driver = driver_factory.create_driver(driver_path, options)

    try:
        # Usage
        new_index_page = IndexPage(driver)
        new_index_page.open()

        new_index_page.select_total_returns_index()
        new_index_page.select_equity_return_type()

        # Get the total number of elements in the select_equity_tri dropdown
        index_value_elements = driver.find_elements(By.XPATH, '//*[@id="ddlHistoricalreturntypeeindex"]/option')
        total_elements = len(index_value_elements)

        # Iterate through different index values and call select_equity_tri
        for index_value in range(1, total_elements + 1):
            new_index_page.select_equity_tri(index_value)
            time.sleep(5)  # Adjust the sleep time as needed

            # Perform other operations (e.g., date selection, submission, etc.)
            new_index_page.choose_start_date("2022", "2", "2", "2")
            #new_index_page.choose_end_date("2023", "8", "1", "3")
            submit_button = driver.find_element(By.ID, 'submit_totalindexhistorical')
            submit_button.click()
            time.sleep(5)

            wait = WebDriverWait(driver, 20)
            table_xpath = '//*[@id="historytotalindex"]'
            wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))

            tbody_xpath = '//*[@id="historytotalindex"]/tbody'
            tbody_element = driver.find_element(By.XPATH, tbody_xpath)

            rows = tbody_element.find_elements(By.TAG_NAME, 'tr')

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) >= 2:
                    date = cells[0].text
                    number = cells[1].text
                    print("Index Value:", index_value)
                    print("Date:", date)
                    print("TOTAL RETURNS INDEX:", number)
    finally:
        # Close the driver when done or if an exception occurs
        driver.quit()





   