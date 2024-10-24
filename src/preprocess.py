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

# Main function to extract and save keywords
if __name__ == "__main__":
    # Load raw tweets
    tweets = load_tweets('./data/World_tweets.json')

    # Extract top 10 keywords
    keywords = extract_keywords(tweets, top_n=10)

    # Save the keywords to a new JSON file
    save_keywords(keywords, './data/World_keywords.json')

    print("Keywords extracted and saved to './data/World_keywords.json'")
