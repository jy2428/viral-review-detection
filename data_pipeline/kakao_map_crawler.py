import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def init_driver(headless=True):
    """Initialize Chrome WebDriver."""
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={ua.random}")
    return webdriver.Chrome(options=options)


def load_more_reviews(driver, max_click=10):
    """Click 'load more reviews' button multiple times."""
    wait = WebDriverWait(driver, 10)
    click_count = 0

    while True:
        try:
            if click_count >= max_click:
                break
            more_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     "#mArticle > div.cont_evaluation > div.evaluation_review > a")
                )
            )
            more_btn.click()
            click_count += 1
            time.sleep(2)
        except:
            break


def parse_reviews(html):
    """Parse and deduplicate review texts from page source."""
    soup = BeautifulSoup(html, "html.parser")
    review_set = set()

    li_elements = soup.select(
        "#mArticle > div.cont_evaluation > div.evaluation_review > ul > li"
    )

    for li in li_elements:
        span = li.select_one("div.comment_info > p > span")
        if span:
            review_set.add(span.text.strip())

    return list(review_set)


def crawl_single_place(place_url, max_click=10):
    """
    Crawl reviews from a single Kakao Map place.
    Returns a list of unique review texts.
    """
    driver = init_driver()
    driver.get(place_url)

    load_more_reviews(driver, max_click)
    reviews = parse_reviews(driver.page_source)

    driver.quit()
    return reviews


def crawl_multiple_places(place_df):
    """
    Crawl reviews for multiple places.
    place_df must contain 'Name' and 'link' columns.
    """
    results = {}

    for idx, row in place_df.iterrows():
        name = row["Name"]
        link = row["link"]
        print(f"[{idx}] Crawling reviews for {name}")
        results[name] = crawl_single_place(link)

    return results
