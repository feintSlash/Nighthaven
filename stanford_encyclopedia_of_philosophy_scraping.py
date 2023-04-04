import requests
from bs4 import BeautifulSoup
import os

# Set the URL of the homepage of the Stanford Encyclopedia of Philosophy
url = 'https://plato.stanford.edu/contents.html'

# Send a GET request to the URL and get the HTML content
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the links on the page that point to articles
article_links = soup.find_all('a', {'class': 'external'})

# Create the "data" folder if it doesn't exist
if not os.path.exists('data'):
    os.mkdir('data')

# Loop through each link, make a request to the page, and extract the content
for link in article_links:
    article_url = link['href']
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')

    # Extract the title of the article
    title = article_soup.find('h1', {'class': 'title'}).text.strip()

    # Extract the authors of the article
    authors = article_soup.find('div', {'class': 'entry-author'}).text.strip()

    # Extract the publication date of the article
    pub_date = article_soup.find('div', {'class': 'entry-published'}).text.strip()

    # Extract the abstract of the article
    abstract = article_soup.find('div', {'class': 'abstract'}).text.strip()

    # Extract the main content of the article
    main_content = article_soup.find('div', {'class': 'entry-content'})

    # Extract the sections of the article and their content
    sections = main_content.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol'])
    section_texts = []
    for section in sections:
        if section.name.startswith('h'):
            section_texts.append('\n\n' + section.text.strip() + '\n\n')
        else:
            section_texts.append(section.text.strip() + '\n')

    # Write the data to a file
    with open(f'data/{title}.txt', 'w', encoding='utf-8') as f:
        f.write(f'Title: {title}\n\n')
        f.write(f'Authors: {authors}\n\n')
        f.write(f'Publication Date: {pub_date}\n\n')
        f.write(f'Abstract: {abstract}\n\n')
        f.write('\n'.join(section_texts))
