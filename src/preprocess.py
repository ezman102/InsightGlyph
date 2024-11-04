import json
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

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



#functions for selector--------------------------------------------------------------------------------
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
            choice = int(input("Select a category by number for preprocessing: ")) - 1
            if 0 <= choice < len(categories):
                category_name = list(categories.keys())[choice]
                return category_name, categories[category_name]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
#----------------------------------------------------------------------------------------------------------



#updated main function to include selector logic
def main():
    category_name, urls = select_category()
    if not urls:
        print("No valid URLs found for the selected category.")
        return
    
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
        #again, dynamically use file name
        keywordJsonFileName = './data/' + category_name + '_keywords.json'
        save_keywords(keywords, keywordJsonFileName)

        print("Keywords extracted and saved to" + keywordJsonFileName)
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: JSON file not found. Check for Scrapping")

# Main function to extract and save keywords
if __name__ == "__main__":
    main()
