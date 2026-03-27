#!/usr/bin/env python3
"""
Golden Home Project — Facebook Auto-Poster
Posts to Facebook Page via mbasic.facebook.com using Selenium.
No official API needed.
"""

import os
import sys
import json
import time
import random
import logging
import pickle
from pathlib import Path
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("ERROR: selenium not installed. Run: pip3 install selenium")
    sys.exit(1)

# --- Config ---
COOKIES_FILE = Path(__file__).parent / "logs" / "fb_cookies.pkl"
LOG_FILE = Path(__file__).parent / "logs" / "posting_log.json"
FB_PAGE_ID = "973754055831729"  # Golden Home Project page ID
MBASIC_URL = f"https://mbasic.facebook.com/page/wall/?id={FB_PAGE_ID}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ghp_fb_poster")


def get_credentials():
    email = os.environ.get("GHP_FB_EMAIL")
    password = os.environ.get("GHP_FB_PASSWORD")
    if not email or not password:
        logger.error("Set GHP_FB_EMAIL and GHP_FB_PASSWORD environment variables")
        sys.exit(1)
    return email, password


def human_delay(min_s=2, max_s=5):
    time.sleep(random.uniform(min_s, max_s))


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver


def save_cookies(driver):
    pickle.dump(driver.get_cookies(), open(COOKIES_FILE, "wb"))
    logger.info("Cookies saved")


def load_cookies(driver):
    if COOKIES_FILE.exists():
        cookies = pickle.load(open(COOKIES_FILE, "rb"))
        driver.get("https://mbasic.facebook.com")
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception:
                pass
        logger.info("Cookies loaded")
        return True
    return False


def login(driver, email, password):
    """Login to mbasic.facebook.com"""
    driver.get("https://mbasic.facebook.com")
    human_delay()

    # Check if already logged in via cookies
    if "mbasic_logout_button" in driver.page_source or "/logout.php" in driver.page_source:
        logger.info("Already logged in via cookies")
        return

    # Fill login form
    try:
        email_field = driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(email)
        human_delay(1, 2)

        pass_field = driver.find_element(By.NAME, "pass")
        pass_field.clear()
        pass_field.send_keys(password)
        human_delay(1, 2)

        login_btn = driver.find_element(By.NAME, "login")
        login_btn.click()
        human_delay(3, 5)

        save_cookies(driver)
        logger.info("Login successful")
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise


def post_to_page(driver, caption, image_path=None):
    """Post to Facebook Page via mbasic"""
    driver.get(MBASIC_URL)
    human_delay(2, 4)

    # Find the post form textarea
    try:
        textarea = driver.find_element(By.NAME, "xc_message")
    except Exception:
        # Alternative selector
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        if textareas:
            textarea = textareas[0]
        else:
            raise Exception("Could not find post textarea on page")

    textarea.clear()
    textarea.send_keys(caption)
    human_delay(2, 3)

    # Upload image if provided
    if image_path and Path(image_path).exists():
        try:
            # Look for photo upload link/button
            photo_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Photo")
            if photo_links:
                photo_links[0].click()
                human_delay(2, 3)

            # Find file input
            file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if file_inputs:
                file_inputs[0].send_keys(str(Path(image_path).resolve()))
                human_delay(3, 5)
                logger.info(f"Image uploaded: {image_path}")
        except Exception as e:
            logger.warning(f"Image upload failed (posting text only): {e}")

    # Submit the post
    submit_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='submit'][name='view_post']")
    if not submit_buttons:
        submit_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")

    if submit_buttons:
        submit_buttons[-1].click()
        human_delay(3, 5)
        logger.info("Post submitted!")
    else:
        raise Exception("Could not find submit button")


def log_result(image_path, success, details):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": "facebook",
        "image": str(image_path) if image_path else None,
        "success": success,
        **details,
    }
    logs = []
    if LOG_FILE.exists():
        try:
            logs = json.loads(LOG_FILE.read_text())
        except json.JSONDecodeError:
            logs = []
    logs.append(log_entry)
    LOG_FILE.write_text(json.dumps(logs, indent=2))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Post to Facebook for Golden Home Project")
    parser.add_argument("--image", help="Path to image file (optional)")
    parser.add_argument("--caption", required=True, help="Path to caption text file OR raw caption")
    args = parser.parse_args()

    caption_path = Path(args.caption)
    if caption_path.exists():
        caption = caption_path.read_text().strip()
    else:
        caption = args.caption

    email, password = get_credentials()
    driver = None

    try:
        driver = create_driver()
        load_cookies(driver)
        login(driver, email, password)
        human_delay(5, 10)
        post_to_page(driver, caption, args.image)
        log_result(args.image, True, {"message": "Posted successfully"})
        print("SUCCESS: Posted to Facebook")
    except Exception as e:
        logger.error(f"Facebook posting failed: {e}")
        log_result(args.image, False, {"error": str(e)})
        sys.exit(1)
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
