"""This file contains the functions used to scrape publicly available data from various sites, in order
to create Books, a custom class.
"""

import bs4
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime


class Book:
    """
    #TODO: Fix class introduction.
    """

    def __init__(self, title, author, rating, rating_count, genres):
        self.title = title
        self.author = author
        self.rating = rating
        self.rating_count = rating_count
        self.genres = genres

    def get_genre_score(self, genre_votes: dict[str: int]) -> float:
        """Gives the book a genre score and returns it, based on the genre votes dictionary.
        The genre score should be a number between 1 and 100
        """
        vote_count = sum(value for value in genre_votes.values())
        score = 0
        for genre in genre_votes:
            if genre in self.genres:
                score += genre_votes[genre]

        return 100 * score / vote_count


def generate_popular_by_date_urls() -> list[str]:
    """ Collects all the "popular by date published"  urls from last year and all available from this year.
    Returns a list of urls.
    """
    urls = []
    current_date = datetime.now().date()
    current_month = current_date.month
    current_year = current_date.year

    months = [i for i in range(1, current_month + 1)]

    for month in months:
        urls.append(f"https://www.goodreads.com/book/popular_by_date/{current_year}/{month}")

    for i in range(1, 13):
        urls.append(f"https://www.goodreads.com/book/popular_by_date/{current_year - 1}/{i}")

    return urls


def get_book_links(urls: list[str]) -> list[str]:
    """ Returns a list of book links based on the "popular by date published" urls.
    """
    book_links = []
    for url in urls:
        soup = get_book_soup(url)
        h3_elements = soup.find_all('h3', class_='Text Text__title3 Text__umber')
        for h3 in h3_elements:
            a_tags = h3.find_all('a', href=True)
            for a_tag in a_tags:
                link = a_tag['href']
                book_links.append(link)

    return book_links


def new_book(book_link: str) -> Book:
    """
    This function should return a Book object containing the book title, author,
    rating, number of ratings, and a list of relevant genres.
    """
    soup = get_book_soup(book_link)  # Assuming you have the necessary functions
    return Book(
        get_title(soup),
        get_author(soup),
        get_rating(soup),
        get_rating_count(soup),
        get_genres(soup)
    )


def create_book_list(book_links: list[str]) -> list[Book]:
    """Returns a list of all the books referred to by links in a list of book links
    """
    books = []
    for book_link in book_links:
        books.append(new_book(book_link))

    return books


def generate_recently_published_books() -> list[Book]:
    """Returns a list of books that were published this year or last year
    """
    urls = generate_popular_by_date_urls()
    book_links = get_book_links(urls)
    return create_book_list(book_links)


def generate_book_links(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all <a> elements with a href attribute containing "/book/show"
    book_links = {f"{link['href']}" for link in soup.find_all('a', href=True) if
                  '/book/show' in link['href']}
    book_links = list(book_links)
    if len(book_links) <= 1:
        return generate_book_links(url)
    else:
        return list(book_links)


def get_book_soup(book_link: str) -> bs4.BeautifulSoup:
    """Returns the given book link's 'soup', i.e. its html content.
    """
    response = requests.get(book_link)
    html_content = response.text
    return BeautifulSoup(html_content, 'html.parser')


def get_title(book_soup: bs4.BeautifulSoup) -> str:
    """Returns the title of the book referred to by its book_soup.
    >>> get_title(get_book_soup("https://www.goodreads.com/book/show/61884987-hello-stranger"))
    'Hello Stranger'
    """
    title = book_soup.find('h1', class_='Text Text__title1')
    return title.get_text()


def get_author(book_soup: bs4.BeautifulSoup) -> str:
    """Returns the name of the author of a book using its link's soup.
    >>> get_author(get_book_soup("https://www.goodreads.com/book/show/61884987-hello-stranger"))
    'Katherine Center'
    """
    return book_soup.find('span', class_="ContributorLink__name").get_text()


def get_genres(book_soup: bs4.BeautifulSoup) -> list[str]:
    """Returns the genres of a book as given by its book link's soup.
    Note that the following doctest may be particular to my computer window size.
    >>> get_genres(get_book_soup("https://www.goodreads.com/book/show/61884987-hello-stranger"))
    ['Romance', 'Fiction', 'Contemporary', 'Contemporary Romance', 'Audiobook', 'Chick Lit', 'Adult']
    """
    genre_buttons = book_soup.find_all('span', class_='BookPageMetadataSection__genreButton')
    genres = []
    for genre in genre_buttons:
        genres.append(genre.get_text())
    return genres


def get_rating(book_soup: bs4.BeautifulSoup) -> float:
    """Returns the rating of a book using its link's soup.
    >>> get_rating(get_book_soup("https://www.goodreads.com/book/show/61884987-hello-stranger"))
    4.1
    """
    rating = float(book_soup.find('div', class_='RatingStatistics__rating').get_text())
    return rating


def get_rating_count(book_soup: bs4.BeautifulSoup) -> int:
    """Returns the number of ratings given to a book using its link's soup.
    >>> get_rating_count(get_book_soup("https://www.goodreads.com/book/show/61884987-hello-stranger"))
    23857
    """
    rating_count_descriptor = book_soup.find('span', {'data-testid': 'ratingsCount'})
    text = rating_count_descriptor.get_text().replace(',', '')
    return int(re.search(r'\d+', text).group())


def get_book_info(book_link: str) -> (str, float, int, int,):
    """
    This function should list containing the book title, the book rating, and the number of ratings,
    plus a sublist of relevant genres.

    >>> get_book_info("https://www.goodreads.com/book/show/61884987-hello-stranger")
    ['Hello Stranger', 'Katherine Center', 4.09, 23857, ['Romance', 'Fiction', 'Contemporary', 'Contemporary Romance', 'Chick Lit', 'Audiobook', 'Adult']]

    """
    soup = get_book_soup(book_link)
    return [get_title(soup), get_author(soup), get_rating(soup), get_rating_count(soup), get_genres(soup)]
