from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Step 1: Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run browser in headless mode (no GUI)
driver = webdriver.Chrome(options=options)

# Step 2: Load the dynamic webpage
url = "https://invoices.rae.gr/%ce%ba%ce%b1%cf%84%ce%b1%cf%87%cf%89%cf%81%ce%b7%ce%bc%ce%ad%ce%bd%ce%b1-%cf%84%ce%b9%ce%bc%ce%bf%ce%bb%cf%8c%ce%b3%ce%b9%ce%b1-%cf%80%cf%81%ce%bf%ce%bc%ce%ae%ce%b8%ce%b5%ce%b9%ce%b1%cf%82-%ce%b7-3/"
driver.get(url)

# Step 3: Wait for the table to load
try:
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "billing_table"))
    )
    print("Table loaded successfully!")
except Exception as e:
    print("Error: Table did not load in time.")
    driver.quit()
    exit()

# Step 4: Extract table headers
headers = [th.text for th in table.find_elements(By.TAG_NAME, "th")]

# Step 5: Extract table rows
rows = table.find_elements(By.TAG_NAME, "tr")
data = []
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    data.append([cell.text.strip() for cell in cells])

# Step 6: Save the data to a CSV file
df = pd.DataFrame(data, columns=headers)
df.to_csv("electricity_tariffs.csv", index=False)

print("Scraping complete! Data saved to 'electricity_tariffs.csv'.")

# Close the browser
driver.quit()
