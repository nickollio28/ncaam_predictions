from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
import csv
import time
import random
import os

START_DATE = datetime(2014, 11, 14)
RANDOM_SLEEP_TIMES = [10,120]
EMAIL = "ollio.nick@gmail.com"
PASSWORD = "PASSWORD"

def setup_driver():
    driver = webdriver.Chrome()
    return driver

def save_data_to_csv(data, filename):
    if data and isinstance(data[0], dict):
        keys = data[0].keys()
        folder_path = "kenpom_archive_data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        full_file_path = os.path.join(folder_path, filename)
        full_file_path = full_file_path.replace(":", "_")  # Replace colons with underscores
        with open(full_file_path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
    else:
        print("Data is empty or not in the expected format.")

def random_sleep(i):
    if (i % random.randint(random.randint(5,10), random.randint(20,35))) == 0:
        t = random.randint(5*60+23, 12*60+4)
        print(f"Random sleep for {t} seconds")
        time.sleep(t)
    if (i % 240 == 0):
        t = 60*60 + random.randint(2, 100)
        print(f"Random sleep for {t%60} minutes")
        time.sleep(60*60 + random.randint(2, 100))

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def get_target_dates(start_date, end_date):
    target_days = (0, 2, 4)  # Monday is 0, Wednesday is 2, Friday is 4
    target_months = (11, 12, 1, 2, 3) # November through March
    dates = []
    for single_date in daterange(start_date, end_date):
        if single_date.weekday() in target_days and single_date.month in target_months:
            dates.append(single_date)
    return dates

def get_season(date):
    year = date.year
    if date.month > 10:  # November or December belong to the beginning of the basketball season
        return f"{year}-{str(year+1)[-2:]}"
    return f"{year-1}-{str(year)[-2:]}"

def check_logged_in(driver):
    try:
        driver.find_element(By.ID, "login")
        return False
    except NoSuchElementException:
        return True

def login(driver, email, password):
    time.sleep(random.randint(1,4))
    driver.find_element(By.NAME, "email").send_keys(email)
    time.sleep(random.randint(1,4))
    driver.find_element(By.NAME, "password").send_keys(password)
    time.sleep(random.randint(1,4))
    driver.find_element(By.NAME, "submit").click()

def extract_data_from_page(driver, date):
    formatted_date = date.strftime("%Y-%m-%d")
    print(f"Extracting data from {formatted_date}")
    url = f"https://kenpom.com/archive.php?d={formatted_date}"
    driver.get(url)

    # Moved check_logged_in here after page load
    if not check_logged_in(driver):
        login(driver, EMAIL, PASSWORD)

    table_rows = driver.find_elements(By.XPATH, "//table[@id='ratings-table']/tbody/tr")
    
    data_list = []
    for row in table_rows:
        # Extract columns for each row
        rk = row.find_element(By.XPATH, ".//td[1]").text
        team = row.find_element(By.XPATH, ".//td[2]").text
        conf = row.find_element(By.XPATH, ".//td[3]").text
        adjem = row.find_element(By.XPATH, ".//td[4]").text
        adjo = row.find_element(By.XPATH, ".//td[5]").text
        adjd = row.find_element(By.XPATH, ".//td[7]").text
        adjt = row.find_element(By.XPATH, ".//td[9]").text
        
        data_list.append({
            "Date": formatted_date,
            "Rk": rk,
            "Team": team,
            "Conf": conf,
            "AdjEM": adjem,
            "AdjO": adjo,
            "AdjD": adjd,
            "AdjT": adjt
        })
    
    return data_list

def main():
    start_date = START_DATE
    end_date = datetime.today()
    dates = get_target_dates(start_date, end_date)
    current_index = 0
    data_by_season = {}

    driver = setup_driver()
    try:
        while current_index < len(dates):
            date = dates[current_index]
            season = get_season(date)

            # Initialize season data list if not already present
            if season not in data_by_season:
                data_by_season[season] = []

            try:
                time.sleep(random.randint(RANDOM_SLEEP_TIMES[0], RANDOM_SLEEP_TIMES[1]))
                data = extract_data_from_page(driver, date)
                data_by_season[season].extend(data)

                # Save the data at the end of a season or when the list of dates is finished
                next_index = current_index + 1
                if next_index >= len(dates) or get_season(dates[next_index]) != season:
                    save_data_to_csv(data_by_season[season], f"data_{season}.csv")

            except Exception as e:
                print(f"An error occurred processing date {date.strftime('%Y-%m-%d')}: {e}")
                # Attempt to save any collected data before moving on
                if data_by_season[season]:
                    save_data_to_csv(data_by_season[season], f"data_{season}_partial.csv")
                    data_by_season[season] = []  # Reset data for the new season

            finally:
                current_index += 1
                random_sleep(current_index)  # Adjust based on your needs

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        driver.quit()
        print("Data saved by season in kenpom_archive_data folder.")

if __name__ == "__main__":
    main()
