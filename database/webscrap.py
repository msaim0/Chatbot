import wikipediaapi
import requests
from bs4 import BeautifulSoup
import nltk
from nltk import pos_tag
# Pending-code
def process_query(query):
    tokens = nltk.word_tokenize(query)
    tagged_tokens = pos_tag(tokens)
    print(tagged_tokens)
    noun_data = []
    for word, tag in tagged_tokens:
        if  tag.startswith('NN') and word.lower() not in ['hi', 'hello']:
            noun_data.append(word)
    return " ".join(noun_data)
# @pending-code
def process_titles(titles):
    return titles[-1]
def get_latest_reddit_post(query):
    # Extracting Nouns
    query_to_search = process_query(query)
    # Create a Wikipedia API object
    wiki = wikipediaapi.Wikipedia('en')  # Specify the language edition ('en' for English)
  # Prompt the user to enter a que
    # Fetch the Wikipedia page
    page = wiki.page(query_to_search)
    if page.exists():
        # Access the page content
        content = page.text
        # Split the content into paragraphs
        paragraphs = content.split('\n\n')
        # Print the first paragraph as the summary
        summary = '\n\n'.join(paragraphs[:1])
        return (f"{query_to_search}: {summary}")
    else:
        return False


# Example usage
