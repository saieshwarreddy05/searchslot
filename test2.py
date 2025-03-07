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

        # Click English
        print("🌎 Clicking 'English' button...")
        try:
            english_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(),'English')]]")))
            english_button.click()
            print("✅ Clicked 'English' button.")
        except Exception as e:
            print("❌ Could not click 'English':", str(e))
            return

        time.sleep(5)  # Increased wait time to allow form to fully load

        print("✅ English selected. Checking if iframe exists...")

        # Detect if form is inside an iframe
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if len(iframes) > 0:
            driver.switch_to.frame(iframes[0])
            print("✅ Switched to iframe.")
        else:
            print("❌ No iframe found.")

        # Wait for form container
        try:
            form_container = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form")))
            print("✅ Form container found.")
        except Exception as e:
            print("❌ Form container not found:", str(e))
            return

        # Locate form fields
        try:
            first_name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[2]/input")))
            last_name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[3]/input")))
            dob_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[4]/input")))
            ssn_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[3]/div[5]/input")))
            print("✅ Found all form fields.")
        except Exception as e:
            print("❌ Form fields not found:", str(e))
            return

        # Fill form details
        print("📝 Filling form details...")
        first_name_field.send_keys(first_name)
        last_name_field.send_keys(last_name)
        dob_field.send_keys(dob)
        ssn_field.send_keys("1234")
        print("✅ Form filled.")

        # Click Log On
        print("🔑 Clicking 'Log On' button...")
        try:
            logon_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/section/div/main/div/section/div[2]/div/div/form/div[2]/div[4]")))
            logon_button.click()
            print("✅ Clicked 'Log On'.")
        except Exception as e:
            print("❌ Could not click 'Log On':", str(e))
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
