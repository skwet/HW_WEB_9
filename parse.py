import requests
from bs4 import BeautifulSoup
import json


def scrap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    return soup


def get_quotes(url):
    quotes = []

    soup = scrap(url)

    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        quotes.append({'tags': tags, 
                       'author': author, 
                       'quote': text})
    return quotes

def get_authors(url):
    authors_list = []

    soup = scrap(url)

    for href in soup.find_all('div', class_='quote'):
        author_href = href.find('a')['href']
        if author_href:
            author_url = 'http://quotes.toscrape.com/' + author_href
            new_soup = scrap(author_url)
            for author in new_soup.find_all('div', class_='author-details'):
                author_name = author.find('h3', class_='author-title').text
                # if author_name not in [existing_author['fullname'] for existing_author in authors]:
                author_born_date = author.find('span', class_='author-born-date').text
                author_born_location = author.find('span', class_='author-born-location').text
                author_description = author.find('div', class_='author-description').text
                author_data = {'fullname': author_name,
                               'born_date': author_born_date,
                               'born_location': author_born_location,
                               'description': author_description.strip()}
                authors_list.append(author_data)

    return authors_list

def main():
    base_url = 'http://quotes.toscrape.com/'

    all_quotes = []
    all_authors = []

    url = base_url
    while url:
        quotes = get_quotes(url)
        authors = get_authors(url)

        all_quotes.extend(quotes)
        for author in authors:
            if author not in all_authors:
                all_authors.append(author)
        
        soup = scrap(url)

        next_page = soup.find('li', class_='next')
        if next_page:
            url = base_url + next_page.find('a')['href']
        else:
            url = None
    
    with open('quotes.json', 'w',encoding='utf-8') as f:
        json.dump(all_quotes, f, indent=4,ensure_ascii=False)
    with open('authors.json', 'w',encoding='utf-8') as f:
        json.dump(all_authors, f, indent=4,ensure_ascii=False)

if __name__ == '__main__':
    main()









