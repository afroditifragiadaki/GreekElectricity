from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Define headers based on provided structure
HEADERS = [
    "Πάροχος",
    "Έτος",
    "Μήνας",
    "Ονομασία Τιμολογίου",
    "Πάγιο (€/μήνα)",
    "Τελική Τιμή Προμήθειας (€/ΚWh)",
    "Πάγιο με Έκπτωση με προϋπόθεση (€/μήνα)",
    "Προϋπόθεση Έκπτωσης Παγίου",
    "Τελική Τιμή Προμήθειας με Έκπτωση με προϋπόθεση (€/ΚWh)",
    "Προϋπόθεση Έκπτωσης Βασικής Τιμής Προμήθειας",
    "Διάρκεια Σύμβασης",
    "Παρατηρήσεις",
]

# Step 1: Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run browser in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

try:
    # Step 2: Load the target webpage
    url = "https://invoices.rae.gr/%ce%ba%ce%b1%cf%84%ce%b1%cf%87%cf%89%cf%81%ce%b7%ce%bc%ce%ad%ce%bd%ce%b1-%cf%84%ce%b9%ce%bc%ce%bf%ce%bb%cf%8c%ce%b3%ce%b9%ce%b1-%cf%80%cf%81%ce%bf%ce%bc%ce%ae%ce%b8%ce%b5%ce%b9%ce%b1%cf%82-%ce%b7-3/"
    driver.get(url)

    # Step 3: Wait for the table to load
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "billing_table"))
    )
    print("Table loaded successfully!")

    # Step 4: Extract all rows
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []

    for row in rows[1:]:  # Skip the header row
        cells = row.find_elements(By.TAG_NAME, "td")

        # Extract all cell data, including hidden cells
        row_data = []
        for cell in cells:
            cell_data = cell.text.strip() if cell.is_displayed() else cell.get_attribute("innerText").strip()
            row_data.append(cell_data)

        # Append only if row_data has data
        if row_data:
            data.append(row_data)

    # Step 5: Align rows to headers
    df = pd.DataFrame(data, columns=HEADERS)
    print(df)

    # Step 6: Save to CSV
    df.to_csv("electricity_tariffs.csv", index=False)
    print("Scraping complete! Data saved to 'electricity_tariffs.csv'.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()

