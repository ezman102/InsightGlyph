#This prototype attempts to combine all 3 processes to offer executional simpliticity and user comfortability

#first off, imports
import json
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import validators  # Ensure URLs are valid

#Scrapper Functions======================================================================
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
#======================================================================================================
#Preprocessing Setup and Functions
# NLTK setup
nltk.data.path.append('./nltk_data')
nltk.download('stopwords', download_dir='./nltk_data')

STOPWORDS = set(stopwords.words('english'))
PUNCTUATION = set(['.', ',', '!', '?', ':', ';', '-', '’', '“', '”', '…'])

# Preprocess text: remove URLs, clean, and split words
def preprocess_text(text):
    """Clean text and split it into words."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r"[^a-zA-Z\s]", '', text)
    words = text.lower().split()
    return [word for word in words if word not in STOPWORDS and word not in PUNCTUATION]

# Extract top N keywords from text data
def extract_keywords(tweets, top_n=10):
    """Extract top N keywords from a list of tweets."""
    all_words = [word for tweet in tweets for word in preprocess_text(tweet)]
    return Counter(all_words).most_common(top_n)

# Load raw tweets from JSON
def load_tweets(filename):
    """Load tweets from a JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Save keywords to a JSON file
def save_keywords(keywords, filename):
    """Save extracted keywords to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(keywords, f, ensure_ascii=False, indent=4)
#=================================================================================================
#Visualization functions
# Load the extracted keywords from a JSON file
def load_keywords(filename):
    """Load keywords from a JSON file and validate the structure."""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ensure the data is a list of [word, frequency] pairs
    if isinstance(data, list) and all(isinstance(item, list) and len(item) == 2 for item in data):
        return data
    else:
        raise ValueError("Invalid JSON structure: Expected a list of [word, frequency] pairs.")

# Generate and display a word cloud
def generate_wordcloud(keywords):
    """Generate and display a word cloud."""
    word_freq = {word: freq for word, freq in keywords}
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Generate and display a bar plot
def generate_bar_plot(keywords):
    """Generate and display a bar plot."""
    words, frequencies = zip(*keywords)

    plt.figure(figsize=(10, 5))
    plt.bar(words, frequencies)
    plt.xlabel('Keywords')
    plt.ylabel('Frequency')
    plt.title('Top Keywords')
    plt.xticks(rotation=45, ha='right')
    plt.show()
#================================================================================
#Selector Functions
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
#===============================================================================================
#MAIN FUNCTION
def main():
    #first, let user select a category
    category_name, urls = select_category()
    if not urls:
        print("No valid URLs found for the selected category.")
        return

    print('-------------------------Proceeding to Scraping-----------------------------------')
    print('Initiating Scraping Process...')
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
    print('----------------------Proceeding to Preprocessing------------------------------')
    print('Initiating Preprocessing...')

    #preprocessing
    
    try:
        #dynamically process user choice and fetch the correct json file
        datajsonFilename = './data/' + category_name + '_tweets.json'

        # Load raw tweets
        print('Loading data from ' + datajsonFilename + ' for preprocessing')
        tweets = load_tweets(datajsonFilename)
        # Extract top 10 keywords
        print('Extracting keywords')
        keywords = extract_keywords(tweets, top_n=10)

        # Save the keywords to a new JSON file
        #dynamically use file name
        keywordJsonFileName = './data/' + category_name + '_keywords.json'
        save_keywords(keywords, keywordJsonFileName)

        print("Keywords extracted and saved to" + keywordJsonFileName)
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: JSON file not found. Check for Scrapping")

    print('----------------------Proceeding to Visualization------------------------------')
    print('Initiating Visualization Process...')

    try:
        # Replace with your actual JSON filename
        # updated logic to dynamically select category json based on user input
        jsonFileName = './data/' + category_name + '_keywords.json'

        #keywords = load_keywords('./data/World_keywords.json')
        print('Loading keywords from ' + jsonFileName )
        keywords = load_keywords(jsonFileName)

        print("Generating Word Cloud...")
        generate_wordcloud(keywords)

        print("Generating Bar Plot...")
        generate_bar_plot(keywords)

        print('----------------------Tasks Completed, Exiting Program------------------------------')

    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: JSON file not found. Check for Scrapping and Preprocessing")

    return

#call main
if __name__ == "__main__":
    main()