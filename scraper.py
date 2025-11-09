"""Main script of Homework 3"""
import json
import os
import re
import time

import requests
from bs4 import BeautifulSoup as bs

def get_book_data(book_url: str) -> dict:
    """
    Return a dictionary containing information about a book from
    toscrape.com site.

    Parameters
    ----------
    book_url : str
        URL of the book page. It must be full URL, e. g.
        "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    """

    book_info = {}

    try:
        response = requests.get(book_url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "book_url": book_url}

    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        book_info["title"] = soup.find("h1").text

        for tr in soup.find("table").find_all("tr"):
            # .replace('\xc2', '') is to delete unexpected 'Â' symbol
            # preceding '£' symbol in a value of a book price
            book_info[tr.find("th").text] = tr.find("td").text.replace(
                '\xc2', '')

        product_description = soup.find(
            "div", attrs={"id": "product_description"}
            )
        
        if product_description is not None:
            book_info["product_description"] = \
                product_description.find_next_sibling("p").text

        book_info["star_rating"] = soup.find(
            "p", class_="star-rating")['class'][1]
    else:
        return {"error": f'Request failed with code {response.status_code}',
                "book_url": book_url}

    return book_info

def scrape_books(is_save: bool = False, books_count: int = -1) -> dict:
    """
    Return information about several books from toscrape.com site.

    Result dictionary contains two elements: the 'books' element with
    information about books and the 'fault_pages' with information
    about some errors of scraping.

    Parameters
    ----------
    is_save : bool
        If True the result list is saved to books_data.txt file in the
        same folder where the running script or Jupyter Notebook is.
        Default value is False.
    books_count : int
        Desired count of books in result list. If -1 (by default) all
        the books will be proccessed.
    """

    result = {"books": [], "fault_pages": []}
    page_number = 1
    pages_in_total = 0
    base_url = 'https://books.toscrape.com/catalogue/'

    while True:
        page_url = f'http://books.toscrape.com/catalogue/page-{page_number}.html'

        try:
            response = requests.get(page_url, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            result["fault_pages"].append({"page_number": page_number,
                                          "error": str(e),
                                          "book_url": page_url})

        if response.status_code == 200:
            soup = bs(response.text, "html.parser")
            pages_in_total = int(re.search(r"\d+$", soup.find(
                "li", class_="current").text.strip()).group(0))

            for li in soup.find("ol", class_="row").find_all("li"):
                # Is it make sense to do a pause to not make the overload on the site?
                time.sleep(0.5)

                result["books"].append(get_book_data(
                    base_url + li.find("a")["href"]))

                if len(result["books"]) == books_count:
                    break
        else:
            result["fault_pages"].append(
                {"page_number": page_number,
                "error": f"Response status code was {response.status_code}",
                "book_url": page_url})

        if page_number == pages_in_total \
                or len(result["books"]) == books_count \
                or (len(result["books"]) == 0
                    and len(result["fault_pages"]) > 5):
            if is_save:
                try:
                    file_path = os.path.dirname(__file__) \
                        + '/books_data.txt'
                except NameError:
                    file_path = 'books_data.txt'

                with open(file_path, 'w', encoding='UTF-8') as f:
                    f.write(json.dumps(result))

            break

        page_number += 1

    return result
