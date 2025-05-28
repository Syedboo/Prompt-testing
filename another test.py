from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to your ChromeDriver
service = Service('/path/to/chromedriver')  # Update this path

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://www.linkedin.com/jobs/search/?currentJobId=4083822464&distance=25&geoId=101165590&keywords=data%20analyst&origin=JOBS_HOME_SEARCH_CARDS"

driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Extract job URLs
job_urls = []
try:
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/jobs/')]//@href")))
    job_links = driver.find_elements(By.XPATH, "//a[contains(@href,'/jobs/')]//@href")
    for link in job_links:
        href = link.get_attribute("href")
        if href and href.startswith("https://www.linkedin.com/jobs/"):
            job_urls.append(href)
except Exception as e:
    print(f"Error extracting job URLs: {e}")

# Deduplicate job URLs
job_urls = list(set(job_urls))

# Extract job descriptions
job_data = []
for job_url in job_urls:
    driver.get(job_url)
    time.sleep(2)  # Allow page to load
    try:
        description = driver.find_element(By.XPATH, "//div[@class='mt4']").text
        job_data.append({
            "url": job_url,
            "description": description
        })
    except Exception as e:
        print(f"Error extracting job content from {job_url}: {e}")

# Close the driver
driver.quit()

# Save data to a CSV file
df = pd.DataFrame(job_data)
df.to_csv("linkedin_jobs.csv", index=False)
print("Data saved to linkedin_jobs.csv")