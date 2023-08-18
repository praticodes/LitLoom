""" The LPP responsible for book recommendations relies on maximizing the genre match and rating scores.
Both scores are defined and calculated in this file.
"""
import math
from books import Book


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


def score_from_ratings_and_count(book) -> float:
    """Gives the inputted book an adjusted rating score based on its rating and rating count.
    The rating score must be between 0 and 100.
    #TODO: Add doctest.
    """
    advantage = book.rating - math.e ** (book.rating_count * 3 / (10 ** 5))
    max_advantage = 1.3
    if advantage <= 0:
        return 0.0
    else:
        return advantage / max_advantage * 100


def get_rating_scores(books: list[Book]) -> dict[Book: float]:
    """Gives each book an adjusted rating score based on its rating and rating count.
    """
    rating_scores = {}
    for book in books:
        rating_scores[book] = score_from_ratings_and_count(book)


def get_genre_scores(books: list[Book]) -> dict[Book: float]:
    """Gives each book a genre score and returns a dictionary of books and genre scores.
    """
    genre_scores = {}
    for book in books:
        genre_scores[book] = book.get_genre_score
