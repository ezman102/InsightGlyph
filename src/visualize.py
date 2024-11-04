import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

#----------------------------------------------------------------------------------------------------------------------
# This section let the user to select a category to be visualized
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
            choice = int(input("Select a category by number to be visualized: ")) - 1
            if 0 <= choice < len(categories):
                category_name = list(categories.keys())[choice]
                return category_name, categories[category_name]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
#--------------------------------------------------------------------------------------------------------------------------------------

#updated the main function to include selector logic
def main():
    category_name, urls = select_category()
    if not urls:
        print("No valid URLs found for the selected category.")
        return

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

    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: JSON file not found. Check for Scrapping and Preprocessing")


# Main function to visualize keywords from JSON
if __name__ == "__main__":
    main()
