import os
import sys
import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "ui_screenshots", "droitdash_features")
os.makedirs(OUTPUT_DIR, exist_ok=True)

backend_proc = None
frontend_proc = None

def is_server_running(url):
    try:
        r = requests.get(url, timeout=1)
        return r.status_code == 200
    except Exception:
        return False

try:
    # 1. Check or start backend
    if not is_server_running("http://127.0.0.1:8000/api/status"):
        print("Starting FastAPI backend on port 8000...")
        backend_cmd = [sys.executable, "-m", "uvicorn", "server:app", "--host", "127.0.0.1", "--port", "8000"]
        backend_proc = subprocess.Popen(backend_cmd, cwd=os.path.join(BASE_DIR, "backend"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for _ in range(25):
            if is_server_running("http://127.0.0.1:8000/api/status"):
                break
            time.sleep(1)

    # 2. Check or start frontend
    if not is_server_running("http://127.0.0.1:5173"):
        print("Starting Vite frontend on port 5173...")
        frontend_cmd = ["cmd", "/c", "npx", "vite", "--port", "5173", "--host", "127.0.0.1"]
        frontend_proc = subprocess.Popen(frontend_cmd, cwd=BASE_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for _ in range(25):
            if is_server_running("http://127.0.0.1:5173"):
                break
            time.sleep(1)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1600,1150")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    print("Navigating to http://127.0.0.1:5173...")
    driver.get("http://127.0.0.1:5173")
    time.sleep(3)

    # 1. Overview
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "01_overview.png"))
    print("Captured 01_overview.png")

    pages = [
        ("Live Prediction", "02_live_prediction.png"),
        ("EDA Insights", "03_eda.png"),
        ("Model Benchmark", "04_model_benchmark.png"),
        ("Word Insights", "05_word_insights.png"),
        ("Bayesian Net", "06_bayesian_net.png"),
        ("Volume Forecast", "07_time_series.png")
    ]

    for label, filename in pages:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if label in btn.text:
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                btn.click()
                time.sleep(1.5)
                break
        
        path = os.path.join(OUTPUT_DIR, filename)
        driver.save_screenshot(path)
        print(f"Captured {path}")

    print("All feature screenshots captured successfully!")

finally:
    if 'driver' in locals() and driver:
        driver.quit()
    if backend_proc:
        backend_proc.terminate()
    if frontend_proc:
        frontend_proc.terminate()
