import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import validators  # Ensure URLs are valid

# Initialize Selenium WebDriver
def init_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

# Scroll and scrape tweets
def scroll_and_scrape(driver, max_scrolls=20):
    tweets = []
    seen_texts = set()

    for _ in range(max_scrolls):
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)  # Adjust sleep time to allow content to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find and collect tweets
        for tweet in soup.find_all('article'):
            text = tweet.find(['div', 'span'], {'data-testid': 'tweetText'})
            if text and text.get_text() not in seen_texts:
                tweets.append(text.get_text())
                seen_texts.add(text.get_text())

    return tweets

# Scrape tweets from a specific account
def scrape_account(url, headless=True):
    if not validators.url(url):
        print(f"Invalid URL: {url}")
        return []

    try:
        driver = init_driver(headless)
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetText']"))
        )
        tweets = scroll_and_scrape(driver)

    finally:
        driver.quit()

    return tweets

# Load category-to-account mapping
def load_categories():
    try:
        with open('categories/categories.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: categories.json not found.")
        return {}

# Let the user select a category
def select_category():
    categories = load_categories()
    if not categories:
        return None, []

    print("Available categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")

    while True:
        try:
            choice = int(input("Select a category by number: ")) - 1
            if 0 <= choice < len(categories):
                category_name = list(categories.keys())[choice]
                return category_name, categories[category_name]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

# Main function to orchestrate the scraping process
def main():
    category_name, urls = select_category()
    if not urls:
        print("No valid URLs found for the selected category.")
        return

    print(f"Scraping tweets for category: {category_name}")
    all_tweets = []

    for url in urls:
        print(f"Scraping {url}...")
        tweets = scrape_account(url, headless=True)
        all_tweets.extend(tweets)

    print(f"Collected {len(all_tweets)} tweets.")
    
    # Save tweets to a JSON file
    with open(f'data/{category_name}_tweets.json', 'w', encoding='utf-8') as f:
        json.dump(all_tweets, f, ensure_ascii=False, indent=4)
    print(f"Tweets saved to 'data/{category_name}_tweets.json'.")

# Run the main function
if __name__ == "__main__":
    main()
