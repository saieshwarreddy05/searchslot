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
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        wait = WebDriverWait(driver, 15)
        print("🚀 Opening Texas DPS Scheduler website...")
        driver.get("https://www.txdpsscheduler.com/")
        time.sleep(3)

        # Click English button
        print("🌎 Clicking 'English' button...")
        try:
            english_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(),'English')]]")))
            english_button.click()
            print("✅ Clicked 'English' button.")
        except Exception as e:
            print("❌ Could not click 'English':", str(e))
            return

        time.sleep(5)
        print("✅ English selected. Waiting for form fields...")

        # Locate form fields using full XPath and send_keys()
        try:
            dl_number_field = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[1]/div/div[1]/div/input")
            first_name_field = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[2]/div/div[1]/div/input")
            last_name_field = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[3]/div/div[1]/div/input")
            dob_field = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[4]/div/div[1]/div/input")
            ssn_field = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[5]/div/div[1]/div/input")
            logon_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/section/div/main/div/section/div[2]/div/div/form/div[2]/div[4]")
            print("✅ Found all form fields.")
        except Exception as e:
            print("❌ Form fields not found:", str(e))
            return

        # Fill form details using send_keys() with delay
        print("📝 Filling form details slowly...")
        time.sleep(3)
        dl_number_field.send_keys(" ")  # Empty space if optional
        time.sleep(3)
        first_name_field.send_keys(first_name)
        time.sleep(3)
        last_name_field.send_keys(last_name)
        time.sleep(3)
        dob_field.send_keys(dob)
        time.sleep(3)
        ssn_field.send_keys("1234")
        print("✅ Form filled.")

        # Click Log On after delay
        print("🔑 Clicking 'Log On' button after 5 sec...")
        time.sleep(5)
        try:
            logon_button.click()
            print("✅ Clicked 'Log On'.")
        except Exception as e:
            print("❌ Could not click 'Log On':", str(e))
            return

        time.sleep(5)

        # Check for which button is enabled (blue button)
        print("📅 Checking which appointment button is active...")
        try:
            existing_appt = driver.find_element(By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/div[5]/div")
            new_appt = driver.find_element(By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/div[3]/div/button/span")
            
            if "blue" in existing_appt.get_attribute("class"):  # Check if it's styled as enabled
                existing_appt.click()
                print("🗓️ Clicked on 'Existing Appointment'.")
            else:
                new_appt.click()
                print("➕ Clicked on 'New Appointment'.")
        except Exception as e:
            print("❌ Error determining which button to click:", str(e))
            return

        time.sleep(5)
        print("✅ Done!")
    
    except Exception as e:
        print("❌ Error:", str(e))
        input("Press Enter to exit (this keeps browser open for debugging)...")  # Keeps browser open
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
