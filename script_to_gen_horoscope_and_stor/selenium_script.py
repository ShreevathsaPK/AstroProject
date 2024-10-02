from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode if you don't need a browser window
chrome_options.add_argument("--no-sandbox")  # Add for additional compatibility
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Create the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the website
driver.get("https://astrotalk.com/freekundli/basic-detail")

# Wait for the page to load
driver.implicitly_wait(10)

# Example: Fill in mobile number
mobile_input = driver.find_element(By.NAME, "mobile")
mobile_number = "7019796860"  # Replace with your mobile number
mobile_input.send_keys(mobile_number)

# Click on the 'Get OTP' button (update the selector accordingly)
get_otp_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Get OTP')]")
get_otp_button.click()

# Wait for the OTP to be sent
time.sleep(30)  # Wait time for OTP to be received (adjust as needed)

# Prompt user for OTP
otp = input("Enter the OTP sent to your mobile: ")

# Fill in the OTP
otp_input = driver.find_element(By.NAME, "otp")  # Update the selector if needed
otp_input.send_keys(otp)

# Click on the 'Submit' button (update the selector accordingly)
submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
submit_button.click()

# Wait for the next page to load after submitting the OTP
time.sleep(10)  # Adjust as necessary

# Now you can scrape the data you need after login
# Example: Scraping some data
# data = driver.find_element(By.ID, "some-data-id").text  # Update the selector based on what you want to scrape
# print(data)

# Quit the driver
driver.quit()
