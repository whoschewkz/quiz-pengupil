import os
import time
import logging
import requests
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================= CONFIG =================
BASE_URL = "http://127.0.0.1:8000/"
LOG_DIR = "test-results"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "test_log.txt"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ================= DRIVER =================
chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

# ================= UTIL =================
def wait_for_server(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            if requests.get(url).status_code == 200:
                return
        except:
            time.sleep(2)
    raise RuntimeError("Server not responding")

def run_test(fn):
    try:
        fn()
        logging.info(f"{fn.__name__}: PASSED")
        print(f"✅ {fn.__name__}")
    except AssertionError as e:
        logging.error(f"{fn.__name__}: FAILED - {e}")
        print(f"❌ {fn.__name__}: {e}")

# ================= LOGIN TESTS =================
def test_login_invalid():
    driver.get(BASE_URL + "login.php")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    ).send_keys("salah")

    driver.find_element(By.ID, "InputPassword").send_keys("salah")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "Register User Gagal" in driver.page_source

def test_login_empty():
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "Data tidak boleh kosong" in driver.page_source

# ================= REGISTER TESTS =================
def test_register_password_mismatch():
    driver.get(BASE_URL + "register.php")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    ).send_keys("newuser")

    driver.find_element(By.ID, "name").send_keys("New User")
    driver.find_element(By.ID, "InputEmail").send_keys("new@mail.com")
    driver.find_element(By.ID, "InputPassword").send_keys("123456")
    driver.find_element(By.ID, "InputRePassword").send_keys("654321")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(2)
    assert "Password tidak sama" in driver.page_source

def test_register_empty():
    driver.get(BASE_URL + "register.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "Data tidak boleh kosong" in driver.page_source

# ================= RUN =================
wait_for_server(BASE_URL)

tests = [
    test_login_invalid,
    test_login_empty,
    test_register_password_mismatch,
    test_register_empty,
]

for t in tests:
    run_test(t)

driver.quit()
