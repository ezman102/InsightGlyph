# **Social Media Keyword Analysis Project**

## **Overview**
This project focuses on scraping tweets from X.com (formerly Twitter), extracting meaningful keywords from the collected tweets, and visualizing them through word clouds and bar plots. The project allows users to select categories (like Music, Sports, or Business) and scrape tweets from predefined accounts, extracting insights and presenting them visually.

---

## **Features**
- **Scrape Tweets** from specific accounts under multiple categories.
- **Preprocess text** to remove stopwords, punctuation, and URLs.
- **Extract keywords** and analyze their frequency.
- **Generate visualizations** such as word clouds and bar plots.
- **Easily extendable** with additional categories or accounts.

---

## **Project Structure**
```
/social-media-keyword-analysis
│
├── /data                        # Stores scraped tweets and extracted keywords
│   ├── World_tweets.json        # Raw tweets from the 'World' category
│   ├── World_keywords.json      # Extracted keywords from World tweets
│
├── /categories                  # Configuration for category-to-account mapping
│   └── categories.json          # Maps categories to X.com accounts
│
├── /nltk_data                   # NLTK data directory for stopwords and tokenizers
│
├── /src                         # Source code directory
│   ├── scraper.py               # Code to scrape tweets using Selenium
│   ├── preprocess.py            # Code to preprocess text and extract keywords
│   └── visualize.py             # Code to generate word clouds and bar plots
│
├── main.ipynb                   # Jupyter notebook for experimenting and EDA
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation
```

---

## **Setup Instructions**

### **Prerequisites**
1. **Python 3.8+** installed.
2. **ChromeDriver** installed and added to your PATH.  
   Download from: https://chromedriver.chromium.org/downloads

### **Install Dependencies**

1. **Install required libraries**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download NLTK Data** (stopwords and tokenizers):
   ```bash
   python -m nltk.downloader stopwords punkt -d ./nltk_data
   ```

---

## **Usage Instructions**

### **1. Run the Scraper**
```bash
python src/scraper.py
```
1. **Select a category** when prompted.
2. The scraper collects tweets from the selected category and saves them as `data/<category>_tweets.json`.

### **2. Extract Keywords from Tweets**
```bash
python src/preprocess.py
```
This script:
1. Loads raw tweets from the `data/` directory.
2. Extracts the top keywords and saves them as `data/<category>_keywords.json`.

### **3. Visualize Keywords**
```bash
python src/visualize.py
```
This script:
1. Loads the extracted keywords from the JSON file.
2. Generates a **word cloud** and **bar plot** to display keyword frequencies.

### **4. Use Jupyter Notebook for EDA (Optional)**
```bash
jupyter notebook main.ipynb
```
- Experiment with scraping, preprocessing, and visualization within the notebook.

---

## **Configuration**
### **Modify `categories.json`**
To **add or modify categories**, update the `categories.json` file located in the `/categories` directory. Example:

```json
{
    "World": ["https://x.com/CNN", "https://x.com/Reuters"],
    "Music": ["https://x.com/billboard", "https://x.com/Spotify"]
}
```

---

## **Example Output**

### **Word Cloud Example:**
- Displays keywords with larger sizes representing higher frequency.

### **Bar Plot Example:**
- Shows the most frequent keywords on the x-axis with their frequency on the y-axis.

---

## **Dependencies**
- **Selenium**: Web scraping automation.
- **BeautifulSoup**: HTML parsing.
- **NLTK**: Natural Language Toolkit for text preprocessing.
- **matplotlib**: Visualization library for bar plots.
- **wordcloud**: Library to generate word clouds.

---

## **License**
This project is licensed under the **MIT License** - see the `LICENSE` file for details.

---

This **README.md** covers all essential aspects of the project, including **setup, usage, configuration, and troubleshooting**. Let me know if you need any further modifications!