"""This file is for testing the performance of the recommendation algorithm(s)
"""
import random
import time
from lpp import get_recommendations_lpp, get_recommendations_sort
from books import Book, create_books_from_csv


def generate_random_genre_votes(count=100) -> list[dict[str: int]]:
    """
    Generates random genre vote dictionaries.
    >>> generate_random_genre_votes()
    """
    dictionaries = []
    genres = [
        'Romance', 'Fiction', 'Contemporary', 'Contemporary Romance', 'Audiobook',
        'Adult', 'Chick Lit', 'Thriller', 'Mystery', 'Mystery Thriller', 'Suspense',
        'Psychological Thriller', 'Nonfiction', 'Memoir', 'Biography', 'Autobiography',
        'Biography Memoir', 'LGBT', 'Horror', 'Literary Fiction', 'Feminist', 'African American',
        'Magical Realism', 'Historical Fiction', 'Science Fiction', 'Mental Health', 'Essays',
        'Humor', 'Sports', 'Christmas', 'Queer', 'New Adult', 'Gothic', 'Classic'
    ]

    for i in range(0, count):
        dictionary = {}
        for genre in genres:
            dictionary[genre] = random.randint(0, 10)
        dictionaries.append(dictionary)

    return dictionaries


def lpp_metrics(book_list: list[Book], genre_votes: dict[str: int]):
    """Measure metrics for the LPP-based algorithm
    """
    start_time = time.time()

    get_recommendations_lpp(book_list, genre_votes)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time


def sort_metrics(book_list: list[Book], genre_votes: dict[str: int]):
    """Measure metrics for the sorting-based algorithm
    """
    start_time = time.time()

    get_recommendations_sort(book_list, genre_votes)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time


def time_test(runs=100) -> None:
    """Test the time performance of both algorithms over 100 repetitions.
    Print the results.
    Preconditions:
    - runs > 0
    - isinstance(runs, int)
    """
    book_list = create_books_from_csv()
    genre_votes_dict = generate_random_genre_votes(runs)
    total_time_lpp = 0
    total_time_sort = 0
    for dictionary in genre_votes_dict:
        total_time_lpp += lpp_metrics(book_list, dictionary)
        total_time_sort += sort_metrics(book_list, dictionary)
    average_time_lpp = total_time_lpp / runs
    average_time_sort = total_time_sort / runs
    print(f"LPP took {average_time_lpp:.10f} seconds")
    print(f"Sort took {average_time_sort:.10f} seconds")


def main():
    time_test(10)


if __name__ == "__main__":
    main()
