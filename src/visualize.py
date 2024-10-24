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

# Main function to visualize keywords from JSON
if __name__ == "__main__":
    try:
        # Replace with your actual JSON filename
        keywords = load_keywords('./data/World_keywords.json')

        print("Generating Word Cloud...")
        generate_wordcloud(keywords)

        print("Generating Bar Plot...")
        generate_bar_plot(keywords)

    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: JSON file not found.")
