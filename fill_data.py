from models import Authors,Quotes
from connect import connection
import json

def fill_authors():
    with open('authors.json', 'r', encoding='utf-8') as authors_file:
        authors_data = json.load(authors_file)
        for author_data in authors_data:
            author = Authors(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

def fill_quotes():
    with open('quotes.json', 'r', encoding='utf-8') as quotes_file:
        quotes_data = json.load(quotes_file)
        for quote_data in quotes_data:
            author = Authors.objects.get(fullname=quote_data['author']).id
            quote = Quotes(
                tags=quote_data['tags'],
                author=author,
                quote=quote_data['quote']
            )
            quote.save()

if __name__ == '__main__':
    connection()
    fill_authors()
    fill_quotes()

