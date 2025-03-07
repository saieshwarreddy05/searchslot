import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def book_dps_appointment(first_name, last_name, dob, email, phone, zip_code, service_type):
    # Setup Selenium WebDriver with fixes
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")

    # Ensure the correct WebDriver is installed
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        wait = WebDriverWait(driver, 15)

        print("🚀 Opening Texas DPS Scheduler website...")
        driver.get("https://www.txdpsscheduler.com/")
        time.sleep(3)  # Ensure page fully loads

        # Locate and click the English button
        print("🌎 Clicking 'English' button...")
        english_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(),'English')]]")))
        driver.execute_script("arguments[0].scrollIntoView();", english_button)
        try:
            english_button.click()
        except:
            driver.execute_script("arguments[0].click();", english_button)
        time.sleep(3)

        print("✅ English selected. Waiting for form fields to load...")

        # Ensure the form fields are loaded before inputting data
        first_name_field = driver.find_element(By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[2]/input")
        last_name_field = driver.find_element(By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[3]/input")
        dob_field = driver.find_element(By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[4]/input")
        ssn_field = driver.find_element(By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[5]/input")

        print("📝 Filling form details...")
        first_name_field.send_keys(first_name)
        last_name_field.send_keys(last_name)
        dob_field.send_keys(dob)
        ssn_field.send_keys("1234")

        print("🔑 Clicking 'Log On' button...")
        logon_button = driver.find_element(By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[4]")
        logon_button.click()
        time.sleep(3)

        print("📅 Checking appointment status...")
        try:
            existing_appt = driver.find_element(By.XPATH, "//button[contains(text(),'EXISTING APPOINTMENT')]")
            existing_appt.click()
            print("🗓️ Existing appointment found.")
        except:
            new_appt = driver.find_element(By.XPATH, "//button[contains(text(),'NEW APPOINTMENT')]")
            new_appt.click()
            print("➕ Booking new appointment.")

        time.sleep(3)

        print("🛠️ Selecting service type...")
        service_xpath = "//button[contains(text(), '{}')]".format(service_type)
        service_button = driver.find_element(By.XPATH, service_xpath)
        service_button.click()
        time.sleep(3)

        print("📨 Filling personal details...")
        driver.find_element(By.NAME, "Email").send_keys(email)
        driver.find_element(By.NAME, "ConfirmEmail").send_keys(email)
        driver.find_element(By.NAME, "PhoneNumber").send_keys(phone)
        driver.find_element(By.NAME, "ZipCode").send_keys(zip_code)

        next_button = driver.find_element(By.XPATH, "//button[contains(text(),'NEXT')]")
        next_button.click()
        time.sleep(3)

        print("📍 Selecting location...")
        location_button = driver.find_element(By.XPATH, "//div[contains(text(),'Fort Worth Mega Center')]")
        location_button.click()
        time.sleep(3)

        print("📆 Selecting earliest available date...")
        date_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'date-button')]")
        if date_buttons:
            date_buttons[0].click()
        time.sleep(3)

        print("⏳ Selecting latest available time...")
        time_slots = driver.find_elements(By.XPATH, "//button[contains(@class, 'time-button')]")
        if time_slots:
            time_slots[-1].click()
        time.sleep(3)

        print("✅ Confirming appointment...")
        confirm_button = driver.find_element(By.XPATH, "//button[contains(text(),'CONFIRM')]")
        confirm_button.click()
        time.sleep(3)

        print("🎉 Appointment successfully booked!")

    except Exception as e:
        print("❌ Error:", str(e))

    finally:
        driver.quit()

# Example usage
book_dps_appointment(
    first_name="John",
    last_name="Doe",
    dob="01/01/1990",
    email="jonaro7653@kaiav.com",
    phone="1234567890",
    zip_code="76120",
    service_type="Change, Replace or Renew Texas DL/PERMIT"
)