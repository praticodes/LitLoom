"""This file contains the functions used to scrape publicly available data from various sites, in order
to create Books, a custom class.
"""
import bs4
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import csv
import math


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
        >>> books = create_books_from_csv()
        >>> votes = {'Fiction': 4, 'Romance': 3, 'Feminism': 2, 'Horror': 1}
        >>> books[17].get_genre_score(votes)
        90.0
        """
        vote_count = sum(value for value in genre_votes.values())
        score = 0
        for genre in genre_votes:
            if genre in self.genres:
                score += genre_votes[genre]
        return 100 * score / vote_count

    def get_rating_score(self) -> float:
        """Gives the inputted book an adjusted rating score based on its rating and rating count.
        The rating score must be between 0 and 100.
        >>> book_list = create_books_from_csv()
        >>> book_list[17].get_rating_score()
        31.99999998434544
        """
        advantage = self.rating - (1 / (math.exp(0.00003 * self.rating_count)) + 4)
        max_advantage = 1
        if advantage <= 0:
            return 0.0
        else:
            return advantage * 100

    def get_combined_score(self, genre_votes: dict[str: int]) -> float:
        """Return the sum of the rating score and genre score
        """
        return self.get_genre_score(genre_votes) + self.get_rating_score()


def genre_match(genre_votes: dict[str: int]) -> dict[str: float]:
    """ Based on the genre_votes dictionary i.e. the votes on which genres reading group members want to read,
    this function generates and returns a dictionary containing the percentage of members who like each genre.

    >>> genre_votes_example = {'horror': 7, 'fantasy': 2, 'romance': 1}
    >>> genre_match(genre_votes_example)
    {'horror': 70.0, 'fantasy': 20.0, 'romance': 10.0}
    """
    vote_count = sum(value for value in genre_votes.values())
    vote_percents = {key: 100 * genre_votes[key] / vote_count for key in genre_votes}
    return vote_percents


def get_genre_scores(books: list[Book]) -> dict[Book: float]:
    """Gives each book a genre score and returns a dictionary of books and genre scores.
    """
    genre_scores = {}
    for book in books:
        genre_scores[book] = book.get_genre_score


def create_books_from_csv() -> list[Book]:
    """
    Return a list of book objectives from a csv file of books and their related information.
    >>> book_list = create_books_from_csv()
    >>> book_list[17].title
    'Lessons in Chemistry'
    """
    books = []
    with open('book_info.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            title, author, rating, rating_count, genres = row[0], row[1], float(row[2]), int(row[3]), eval(row[4])
            book = Book(title, author, rating, rating_count, genres)
            books.append(book)

    return books


def sort_books_by_combined_score(book_list: list[Book], genre_votes: dict[str: int]) -> None:
    """
    Sort the books by their combined score using insertion sort, given the genre votes.
    >>> books = create_books_from_csv()
    >>> votes = {'Fiction': 4, 'Romance': 3, 'Feminism': 2, 'Horror': 1, 'Thriller': 2}
    >>> sort_books_by_combined_score(books, votes)
    >>> all(books[i].get_combined_score(votes) <= books[i + 1].get_combined_score(votes) for i in range(0, len(books) - 2))
    True
    """
    for i in range(1, len(book_list)):
        current_book = book_list[i]
        current_score = current_book.get_combined_score(genre_votes)

        j = i - 1
        while j >= 0 and current_score < book_list[j].get_combined_score(genre_votes):
            book_list[j + 1] = book_list[j]
            j -= 1

        book_list[j + 1] = current_book


def generate_popular_by_date_urls() -> list[str]:
    """ Collects all the "popular by date published"  urls from last year and all available from this year.
    Returns a list of urls.
    >>> recent = generate_popular_by_date_urls()
    >>> len(recent)
    2
    """
    urls = []
    current_date = datetime.now().date()
    current_month = current_date.month
    current_year = current_date.year

    months = [i for i in range(current_month - 2, current_month)]

    for month in months:
        urls.append(f"https://www.goodreads.com/book/popular_by_date/{current_year}/{month}")

    return urls


def get_book_links(urls: list[str], book_links=None) -> list[str]:
    """ Returns a list of book links based on the "popular by date published" urls.
    >>> urls = ['https://www.goodreads.com/book/popular_by_date/2023/7','https://www.goodreads.com/book/popular_by_date/2023/6']
    >>> len(get_book_links(urls))
    30
    """
    if book_links is None:
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
    >>> SevenHusbands = new_book('https://www.goodreads.com/book/show/32620332-the-seven-husbands-of-evelyn-hugo')
    >>> isinstance(SevenHusbands, Book)
    True
    >>> SevenHusbands.author
    'Taylor Jenkins Reid'
    >>> SevenHusbands.rating
    4.44
    """
    soup = get_book_soup(book_link)
    return Book(
        get_title(soup),
        get_author(soup),
        get_rating(soup),
        get_rating_count(soup),
        get_genres(soup)
    )


def create_book_list(book_links: list[str]) -> list[Book]:
    """Returns a list of all the books referred to by links in a list of book links
    >>> book_links = ['https://www.goodreads.com/book/show/61884987-hello-stranger', 'https://www.goodreads.com/book/show/59651557-under-one-roof', 'https://www.goodreads.com/book/show/58293924-book-of-night', 'https://www.goodreads.com/book/show/59345253-something-wilder']
    >>> book_list = create_book_list(book_links)
    >>> len(book_list) == 4
    True
    >>> book_list[0].title
    'Hello Stranger'
    """
    books = []
    for book_link in book_links:
        book = new_book(book_link)
        if book.rating > 0.0:
            books.append(book)

    return books


def generate_recently_published_books() -> list[Book]:
    """Returns a list of books that were published this year or last year
    >>> generate_recently_published_books()
    'None Of This is True'
    """
    urls = ['https://www.goodreads.com/book/popular_by_date/2023/8']  # generate_popular_by_date_urls()
    book_links = get_book_links(urls)
    return create_book_list(book_links)


def get_book_soup(book_link: str) -> bs4.BeautifulSoup:
    """Returns the given book link's 'soup', i.e. its html content.
    >>> get_book_soup('https://www.goodreads.com/book/show/62022434-things-we-hide-from-the-light') is not None
    True
    >>> get_book_soup('https://www.goodreads.com/book/show/58065033-lessons-in-chemistry') is not None
    True
    >>> get_book_soup('https://www.goodreads.com/book/show/58733693-remarkably-bright-creatures') is not None
    True
    """
    response = requests.get(book_link)
    html_content = response.text
    return BeautifulSoup(html_content, 'html.parser')


def get_book_title(url) -> str:
    """
    Returns a book's title from its url
    """
    parts = url.split('/')
    last_part_section = url.split('-')[1:]
    title = ''
    for part in last_part_section:
        title += part.capitalize()
        title += ''
    return title


def get_title(book_soup: bs4.BeautifulSoup) -> str:
    """Returns the title of the book referred to by its book_soup.
    >>> get_title(get_book_soup('https://www.goodreads.com/book/show/58733693-remarkably-bright-creatures'))
    'Remarkably Bright Creatures'
    >>> get_title(get_book_soup('https://www.goodreads.com/book/show/61169384-playing-hard-to-get'))
    'Playing Hard to Get'
    >>> get_title(get_book_soup('https://www.goodreads.com/book/show/60495147-nine-liars'))
    'Nine Liars'
    >>> get_title(get_book_soup('https://www.goodreads.com/book/show/60316881-the-headmaster-s-list'))
    "The Headmaster's List"
    >>> get_title(get_book_soup('https://www.goodreads.com/book/show/61398911-girl-forgotten'))
    'Girl Forgotten'
    """
    # Find the div with class "BookPageTitleSection"
    title_div = book_soup.find("div", class_="BookPageTitleSection")
    if title_div is not None:
        title = title_div.get_text()
        if '#' not in title_div.get_text():
            return title
        else:
            return title.split('#')[1][1:]
    return 'Title Unavailable'


def get_author(book_soup: bs4.BeautifulSoup) -> str:
    """Returns the name of the author of a book using its link's soup.
    >>> get_author(get_book_soup('https://www.goodreads.com/book/show/61884987-hello-stranger'))
    'Katherine Center'
    >>> get_author(get_book_soup('https://www.goodreads.com/book/show/58733693-remarkably-bright-creatures'))
    'Shelby Van Pelt'
    >>> get_author(get_book_soup('https://www.goodreads.com/book/show/59912428-mad-honey'))
    'Jodi Picoult'
    >>> get_author(get_book_soup('https://www.goodreads.com/book/show/32620332-the-seven-husbands-of-evelyn-hugo'))
    'Taylor Jenkins Reid'
    """
    span_tag = book_soup.find('span', class_='ContributorLink__name', attrs={'data-testid': 'name'})
    if span_tag is None:
        return 'Author name not found.'
    author_name = span_tag.get_text()
    return author_name


def get_genres(book_soup: bs4.BeautifulSoup) -> list[str]:
    """Returns the genres of a book as given by its book link's soup.
    Note that the following doctest may be particular to my computer window size.
    >>> get_genres(get_book_soup("https://www.goodreads.com/book/show/61884987-hello-stranger"))
    ['Romance', 'Fiction', 'Contemporary', 'Contemporary Romance', 'Chick Lit', 'Audiobook', 'Adult']
    >>> get_genres(get_book_soup('https://www.goodreads.com/book/show/32620332-the-seven-husbands-of-evelyn-hugo'))
    ['Fiction', 'Romance', 'Historical Fiction', 'LGBT', 'Contemporary', 'Audiobook', 'Adult']
    """
    genre_buttons = book_soup.find_all('span', class_='BookPageMetadataSection__genreButton')
    genres = []
    for genre in genre_buttons:
        if genre is not None:
            genres.append(genre.get_text())
    return genres


def get_rating(book_soup: bs4.BeautifulSoup) -> float:
    """Returns the rating of a book using its link's soup.
    >>> get_rating(get_book_soup('https://www.goodreads.com/book/show/61884987-hello-stranger'))
    4.09
    >>> get_rating(get_book_soup('https://www.goodreads.com/book/show/32620332-the-seven-husbands-of-evelyn-hugo'))
    4.44
    >>> get_rating(get_book_soup('https://www.goodreads.com/book/show/60435878-carrie-soto-is-back'))
    4.23
    >>> get_rating(get_book_soup('https://www.goodreads.com/book/show/62971668-someone-else-s-shoes'))
    3.99
    """
    value = book_soup.find('div', class_="RatingStatistics__rating")
    if value is None:
        return 0.0
    else:
        return float(value.get_text())


def get_rating_count(book_soup: bs4.BeautifulSoup) -> int:
    """Returns the number of ratings given to a book using its link's soup.
    >>> get_rating_count(get_book_soup('https://www.goodreads.com/book/show/61884987-hello-stranger'))
    23926
    >>> get_rating_count(get_book_soup('https://www.goodreads.com/book/show/32620332-the-seven-husbands-of-evelyn-hugo'))
    2418584
    """
    rating_count_descriptor = book_soup.find('span', {'data-testid': 'ratingsCount'})
    if rating_count_descriptor is None:
        return 1
    text = rating_count_descriptor.get_text().replace(',', '')
    return int(re.search(r'\d+', text).group())


def get_book_info(book_link: str) -> (str, float, int, int,):
    """
    This function should list containing the book title, the book rating, and the number of ratings,
    plus a sublist of relevant genres.

    >>> get_book_info("https://www.goodreads.com/book/show/61884987-hello-stranger")
    ['Hello Stranger', 'Katherine Center', 4.08, 24236, ['Romance', 'Fiction', 'Contemporary', 'Contemporary Romance', 'Chick Lit', 'Audiobook', 'Adult']]
    """
    soup = get_book_soup(book_link)
    return [get_title(soup), get_author(soup), get_rating(soup), get_rating_count(soup), get_genres(soup)]


def get_book_info_mass(urls: list[str]) -> list[list]:
    """ Return from a list of book links a list of lists in which each list contains a list of the book information for a different book.
    """
    book_list = []
    for url in urls:
        book_list.append(get_book_info(url))
    return book_list


def write_to_csv(book_info_list, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(book_info_list)  # Write book info


def remove_invalid_entries() -> None:
    """Remove entries from a csv file that start with 'Title Unavailable'
    """
    with open('book_info.csv', 'r', newline='', encoding='utf-8') as csvfile:
        rows = list(csv.reader(csvfile))

    with open('book_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        for row in rows:
            if row and not row[0].startswith('Title Unavailable'):
                csv_writer.writerow(row)


def main():
    remove_invalid_entries()


# This block ensures that the main function is only executed when the script is run directly.
if __name__ == "__main__":
    main()
