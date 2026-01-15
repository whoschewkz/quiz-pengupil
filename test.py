import os
import time
import logging
import requests
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================= SETUP =================
BASE_URL = "http://127.0.0.1:8000/"
LOG_DIR = "test-results"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "test_log.txt"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

test_results = []

def wait_for_server(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            if requests.get(url).status_code == 200:
                return True
        except:
            time.sleep(2)
    raise RuntimeError("Server tidak berjalan")

def run_test(fn):
    try:
        fn()
        test_results.append((fn.__name__, "PASSED"))
        logging.info(f"{fn.__name__}: PASSED")
    except AssertionError as e:
        test_results.append((fn.__name__, "FAILED", str(e)))
        logging.error(f"{fn.__name__}: FAILED - {e}")

# ================= LOGIN TEST =================
def test_login_valid():
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "InputPassword").send_keys("Test@123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "Not Found" not in driver.page_source

def test_login_invalid():
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.ID, "username").send_keys("wronguser")
    driver.find_element(By.ID, "InputPassword").send_keys("WrongPass")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "Register User Gagal" in driver.page_source

def test_login_empty():
    driver.get(BASE_URL + "login.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "Data tidak boleh kosong" in driver.page_source

# ================= REGISTER TEST =================
def test_register_valid():
    driver.get(BASE_URL + "register.php")
    driver.find_element(By.ID, "name").send_keys("New User")
    driver.find_element(By.ID, "InputEmail").send_keys("newuser@example.com")
    driver.find_element(By.ID, "username").send_keys("newuser")
    driver.find_element(By.ID, "InputPassword").send_keys("Test@123")
    driver.find_element(By.ID, "InputRePassword").send_keys("Test@123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "Not Found" not in driver.page_source

def test_register_existing_user():
    driver.get(BASE_URL + "register.php")
    driver.find_element(By.ID, "name").send_keys("Existing User")
    driver.find_element(By.ID, "InputEmail").send_keys("existing@example.com")
    driver.find_element(By.ID, "username").send_keys("existinguser")
    driver.find_element(By.ID, "InputPassword").send_keys("Test@123")
    driver.find_element(By.ID, "InputRePassword").send_keys("Test@123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    assert "Username sudah terdaftar" in driver.page_source

def test_register_password_mismatch():
    driver.get(BASE_URL + "register.php")
    driver.find_element(By.ID, "name").send_keys("Another User")
    driver.find_element(By.ID, "InputEmail").send_keys("another@example.com")
    driver.find_element(By.ID, "username").send_keys("anotheruser")
    driver.find_element(By.ID, "InputPassword").send_keys("Test@123")
    driver.find_element(By.ID, "InputRePassword").send_keys("WrongPass")
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
    test_login_valid,
    test_login_invalid,
    test_login_empty,
    test_register_valid,
    test_register_existing_user,
    test_register_password_mismatch,
    test_register_empty,
]

for t in tests:
    run_test(t)

print("\n=== TEST RESULTS ===")
for r in test_results:
    print(r)

driver.quit()
