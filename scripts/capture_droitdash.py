import os
import time
from selenium import webdriver

os.makedirs("outputs/ui_screenshots", exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1600,1180")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

try:
    print("Navigating to http://localhost:5173...")
    driver.get("http://localhost:5173")
    time.sleep(3)
    
    screenshot_path = "outputs/ui_screenshots/droitdash_final.png"
    driver.save_screenshot(screenshot_path)
    print(f"Captured {screenshot_path}: {os.path.getsize(screenshot_path)} bytes")
finally:
    driver.quit()
