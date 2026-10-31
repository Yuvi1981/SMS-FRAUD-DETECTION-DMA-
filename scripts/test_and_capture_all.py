import os
import sys
import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "ui_screenshots", "droitdash_features")
os.makedirs(OUTPUT_DIR, exist_ok=True)

test_results = {}

def log_test(name, passed, detail=""):
    test_results[name] = {"passed": passed, "detail": detail}
    status = "PASS [OK]" if passed else "FAIL [X]"
    print(f"[{status}] {name} - {detail}")

print("=== Starting Full-Stack End-to-End Feature Verification ===")

# 1. Start FastAPI Backend Server
backend_cmd = [sys.executable, "-m", "uvicorn", "server:app", "--host", "127.0.0.1", "--port", "8000"]
backend_proc = subprocess.Popen(backend_cmd, cwd=os.path.join(BASE_DIR, "backend"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 2. Start Vite Dev Server
frontend_cmd = ["cmd", "/c", "npx", "vite", "--port", "5173", "--host", "127.0.0.1"]
frontend_proc = subprocess.Popen(frontend_cmd, cwd=BASE_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

driver = None
try:
    # Wait for backend (port 8000)
    print("Waiting for FastAPI backend to be ready on http://127.0.0.1:8000/api/status...")
    backend_ready = False
    for _ in range(30):
        try:
            r = requests.get("http://127.0.0.1:8000/api/status", timeout=1)
            if r.status_code == 200:
                backend_ready = True
                break
        except Exception:
            pass
        time.sleep(1)
    
    if not backend_ready:
        raise RuntimeError("FastAPI backend failed to start on port 8000")
    print("FastAPI backend is ready!")

    # Wait for frontend (port 5173)
    print("Waiting for Vite frontend to be ready on http://127.0.0.1:5173...")
    frontend_ready = False
    for _ in range(30):
        try:
            r = requests.get("http://127.0.0.1:5173", timeout=1)
            if r.status_code == 200:
                frontend_ready = True
                break
        except Exception:
            pass
        time.sleep(1)

    if not frontend_ready:
        raise RuntimeError("Vite frontend failed to start on port 5173")
    print("Vite frontend is ready!")

    # 3. Setup Selenium Headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1600,1150")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:5173")
    time.sleep(3)

    # Helper function to click sidebar navigation button
    def navigate_to(label):
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if label in btn.text:
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                btn.click()
                time.sleep(1.2)
                return True
        return False

    # -------------------------------------------------------------------------
    # TEST 1: Overview Dashboard
    # -------------------------------------------------------------------------
    page_text = driver.find_element(By.TAG_NAME, "body").text
    has_total = "5,169" in page_text
    has_prev = "12.63%" in page_text
    has_f1 = "0.9653" in page_text
    log_test("Overview KPIs", has_total and has_prev and has_f1, f"Total 5,169: {has_total}, Prev 12.63%: {has_prev}, F1 0.9653: {has_f1}")
    
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "01_overview.png"))
    print("Captured 01_overview.png")

    # -------------------------------------------------------------------------
    # TEST 2: Live Prediction & Explainability
    # -------------------------------------------------------------------------
    navigate_to("Live Prediction")
    time.sleep(1.5)

    # Click Preset 1 (Spam)
    preset_buttons = driver.find_elements(By.TAG_NAME, "button")
    for b in preset_buttons:
        if "Example 1: Lottery Spam" in b.text:
            b.click()
            time.sleep(1)
            break

    # Click Classify SMS
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if "Classify SMS" in b.text:
            b.click()
            time.sleep(1.5)
            break

    pred_text = driver.find_element(By.TAG_NAME, "body").text
    spam_verdict = "SPAM DETECTED" in pred_text
    why_chips = "Why did the model decide this?" in pred_text
    consensus = "Side-by-Side Model Consensus" in pred_text
    log_test("Live Prediction - Spam Test", spam_verdict and why_chips and consensus, 
             f"SPAM verdict: {spam_verdict}, Explainability chips: {why_chips}, Consensus: {consensus}")

    # Now test Preset 2 (Ham)
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if "Example 2: Study Meetup" in b.text:
            b.click()
            time.sleep(1)
            break
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if "Classify SMS" in b.text:
            b.click()
            time.sleep(1.5)
            break

    pred_text_ham = driver.find_element(By.TAG_NAME, "body").text
    ham_verdict = "HAM (LEGITIMATE)" in pred_text_ham
    log_test("Live Prediction - Ham Test", ham_verdict, f"HAM verdict: {ham_verdict}")

    driver.save_screenshot(os.path.join(OUTPUT_DIR, "02_live_prediction.png"))
    print("Captured 02_live_prediction.png")

    # -------------------------------------------------------------------------
    # TEST 3: EDA Insights
    # -------------------------------------------------------------------------
    navigate_to("EDA Insights")
    time.sleep(1.5)

    # Tab 1: Length Distribution (default)
    eda_text = driver.find_element(By.TAG_NAME, "body").text
    has_length_chart = "Character Length Distribution" in eda_text
    log_test("EDA - Length Distribution", has_length_chart, "Length chart rendered")

    # Click Class Balance Summary Tab
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if "Class Balance" in b.text:
            b.click()
            time.sleep(1)
            break
    eda_text_bal = driver.find_element(By.TAG_NAME, "body").text
    has_bal_table = "Corpus Summary Statistics" in eda_text_bal and "4,516" in eda_text_bal
    log_test("EDA - Class Balance Summary", has_bal_table, f"Stats table verified: {has_bal_table}")

    # Click Chi2 Top Terms Tab
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if "Chi²" in b.text:
            b.click()
            time.sleep(1)
            break
    eda_text_chi2 = driver.find_element(By.TAG_NAME, "body").text
    has_chi2 = "claim" in eda_text_chi2 or "free" in eda_text_chi2 or "numtoken" in eda_text_chi2
    log_test("EDA - Chi-Square Terms", has_chi2, f"Chi2 terms verified: {has_chi2}")

    # Click Sample Messages Explorer Tab
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if "Sample Messages" in b.text:
            b.click()
            time.sleep(1)
            break

    # Filter by Spam
    selects = driver.find_elements(By.TAG_NAME, "select")
    for s in selects:
        if "All" in s.text:
            s.send_keys("Spam Only")
            time.sleep(1)
            break

    eda_text_samples = driver.find_element(By.TAG_NAME, "body").text
    has_samples = "Interactive Corpus Explorer" in eda_text_samples and "SPAM" in eda_text_samples
    log_test("EDA - Corpus Explorer & Filter", has_samples, f"Corpus samples loaded: {has_samples}")

    driver.save_screenshot(os.path.join(OUTPUT_DIR, "03_eda.png"))
    print("Captured 03_eda.png")

    # -------------------------------------------------------------------------
    # TEST 4: Model Benchmark
    # -------------------------------------------------------------------------
    navigate_to("Model Benchmark")
    time.sleep(1.5)

    bench_text = driver.find_element(By.TAG_NAME, "body").text
    has_logreg = "Logistic Regression" in bench_text
    has_nb = "Naive Bayes" in bench_text
    has_knn = "k-Nearest Neighbors" in bench_text
    has_bn = "Bayesian Network" in bench_text
    has_rationale = "Champion Selection Rationale" in bench_text
    log_test("Model Benchmark Cross-Evaluation", 
             has_logreg and has_nb and has_knn and has_bn and has_rationale,
             f"LR: {has_logreg}, NB: {has_nb}, KNN: {has_knn}, BN: {has_bn}, Rationale: {has_rationale}")

    # Switch Metric Dropdown to Precision
    metric_select = driver.find_elements(By.TAG_NAME, "select")
    for s in metric_select:
        if "F1-Score" in s.text:
            s.send_keys("Precision")
            time.sleep(1)
            break

    driver.save_screenshot(os.path.join(OUTPUT_DIR, "04_model_benchmark.png"))
    print("Captured 04_model_benchmark.png")

    # -------------------------------------------------------------------------
    # TEST 5: Word Insights
    # -------------------------------------------------------------------------
    navigate_to("Word Insights")
    time.sleep(1.5)

    # Search for "claim"
    word_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Search word']")
    word_input.clear()
    word_input.send_keys("claim")
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if "Lookup Token" in b.text:
            b.click()
            time.sleep(1)
            break

    words_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    has_claim_lookup = "claim" in words_text and "multiplies" in words_text and "spam" in words_text
    has_spam_drivers = "spam drivers" in words_text
    has_ham_drivers = "ham drivers" in words_text
    log_test("Word Insights - Odds Ratio Lookup", has_claim_lookup and has_spam_drivers and has_ham_drivers,
             f"Claim lookup: {has_claim_lookup}, Spam drivers table: {has_spam_drivers}, Ham drivers: {has_ham_drivers}")

    driver.save_screenshot(os.path.join(OUTPUT_DIR, "05_word_insights.png"))
    print("Captured 05_word_insights.png")

    # -------------------------------------------------------------------------
    # TEST 6: Bayesian Net
    # -------------------------------------------------------------------------
    navigate_to("Bayesian Net")
    time.sleep(1.5)

    # Click "Urgent Financial Bait" preset
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if "Urgent Financial Bait" in b.text:
            b.click()
            time.sleep(1)
            break

    bn_text = driver.find_element(By.TAG_NAME, "body").text
    has_high_spam = "SPAM" in bn_text and ("99." in bn_text or "100" in bn_text)
    has_cpt = "Conditional Probability Table" in bn_text
    has_dag = "Directed Acyclic Graph" in bn_text
    log_test("Bayesian Network - Financial Bait Preset", has_high_spam and has_cpt and has_dag,
             f"Posterior Spam high: {has_high_spam}, CPT: {has_cpt}, DAG: {has_dag}")

    # Click "Clean Conversational SMS" preset
    for b in driver.find_elements(By.TAG_NAME, "button"):
        if "Clean Conversational" in b.text:
            b.click()
            time.sleep(1)
            break

    bn_text_clean = driver.find_element(By.TAG_NAME, "body").text
    has_low_spam = "HAM" in bn_text_clean and ("0." in bn_text_clean)
    log_test("Bayesian Network - Clean SMS Preset", has_low_spam, f"Posterior Ham verdict: {has_low_spam}")

    driver.save_screenshot(os.path.join(OUTPUT_DIR, "06_bayesian_net.png"))
    print("Captured 06_bayesian_net.png")

    # -------------------------------------------------------------------------
    # TEST 7: Volume Forecast
    # -------------------------------------------------------------------------
    navigate_to("Volume Forecast")
    time.sleep(1.5)

    ts_text = driver.find_element(By.TAG_NAME, "body").text
    has_sim_notice = "SIMULATED Timestamps" in ts_text
    has_365d = "365-Day Daily Spam Volume" in ts_text
    has_arima = "30-Day Holdout Forecast (ARIMA 1,1,1)" in ts_text
    has_metrics = "Forecast Error Comparison" in ts_text and "11.2%" in ts_text
    log_test("Volume Forecast - 365d & ARIMA Projections", 
             has_sim_notice and has_365d and has_arima and has_metrics,
             f"Simulated notice: {has_sim_notice}, 365d series: {has_365d}, ARIMA forecast: {has_arima}, Metrics: {has_metrics}")

    driver.save_screenshot(os.path.join(OUTPUT_DIR, "07_time_series.png"))
    print("Captured 07_time_series.png")

    print("\n=== SUMMARY OF ALL FEATURE TESTS ===")
    all_passed = True
    for name, res in test_results.items():
        pass_str = "PASS" if res["passed"] else "FAIL"
        if not res["passed"]:
            all_passed = False
        print(f"[{pass_str}] {name}: {res['detail']}")
    
    if all_passed:
        print("\nALL 7 FEATURES EXECUTABLE AND PRODUCING CORRECT OUTPUTS!")
    else:
        print("\nSOME TESTS FAILED! Review details above.")

finally:
    if driver:
        driver.quit()
    print("Terminating background servers...")
    backend_proc.terminate()
    frontend_proc.terminate()
    try:
        backend_proc.wait(timeout=3)
        frontend_proc.wait(timeout=3)
    except Exception:
        backend_proc.kill()
        frontend_proc.kill()
    print("Verification completed cleanly.")
