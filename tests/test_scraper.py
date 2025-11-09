import json
import os
import pytest
from scraper import scrape_books
from scraper import get_book_data

keys = ['title', 'UPC', 'Product Type', 'Price (excl. tax)',
    'Price (incl. tax)', 'Tax', 'Availability', 'Number of reviews',
    'product_description', 'star_rating']

with open(os.path.dirname(os.path.dirname(__file__)) + '/artifacts/books_data.txt', 'r') as f:
    data = json.load(f)

# @pytest.mark.parametrize("url", [
#     ('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'),
#     ('https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html')
#     ])
# def test_expected_keys(url):
#     res = get_book_data(url)
    
#     for key in res.keys():
#         assert key in keys


@pytest.mark.parametrize("book", data["books"])
def test_expected_keys(book):
    for key in book.keys():
        assert key in keys

def test_count_of_books():
    # assert len(scrape_books(False, 5)["books"]) == 5
    assert len(data["books"]) == 1000

# @pytest.mark.parametrize("url", [
#     ('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'),
#     ('https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html')
#     ])
# def test_values_are_correct(url):
#     res = get_book_data(url)
    
#     assert res['star_rating'] in ['One', 'Two', 'Three', 'Four', 'Five']

@pytest.mark.parametrize("book", data["books"])
def test_values_are_correct(book):
    assert book['star_rating'] in ['One', 'Two', 'Three', 'Four', 'Five']
