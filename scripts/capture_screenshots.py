import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.makedirs("outputs/ui_screenshots", exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1600,1100")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
driver.set_window_size(1600, 1100)

def wait_for_streamlit_ready(driver, timeout=10):
    """Waits for Streamlit script runner to finish and DOM to settle."""
    time.sleep(1.0)
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            status_widgets = driver.find_elements(By.CSS_SELECTOR, "[data-testid='stStatusWidget']")
            skeletons = driver.find_elements(By.CSS_SELECTOR, "[data-testid='stSkeleton']")
            if not status_widgets and not skeletons:
                break
        except Exception:
            pass
        time.sleep(0.5)
    time.sleep(1.5)

try:
    print("Navigating to http://localhost:8501...")
    driver.get("http://localhost:8501")
    wait_for_streamlit_ready(driver, 10)

    pages = [
        ("Overview", "01_overview.png"),
        ("Live Prediction", "02_live_prediction.png"),
        ("EDA", "03_eda.png"),
        ("Model Comparison", "04_model_comparison.png"),
        ("Word Insights", "05_word_insights.png"),
        ("Bayesian Network", "06_bayesian_network.png"),
        ("Time Series", "07_time_series.png")
    ]

    for page_name, filename in pages:
        print(f"Selecting page: {page_name} -> {filename}...")
        
        # Click corresponding radio label
        radio_labels = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='stRadio'] label")
        clicked = False
        for lbl in radio_labels:
            if lbl.text.strip().lower() == page_name.lower():
                driver.execute_script("arguments[0].scrollIntoView(true);", lbl)
                lbl.click()
                clicked = True
                break
                
        if not clicked:
            for lbl in radio_labels:
                if page_name.lower() in lbl.text.lower():
                    driver.execute_script("arguments[0].scrollIntoView(true);", lbl)
                    lbl.click()
                    clicked = True
                    break

        wait_for_streamlit_ready(driver, 10)

        # Save screenshot
        target_path = os.path.join("outputs", "ui_screenshots", filename)
        driver.save_screenshot(target_path)
        print(f"Captured: {target_path} (size: {os.path.getsize(target_path)} bytes)")

finally:
    driver.quit()
    print("All screenshots successfully captured!")
