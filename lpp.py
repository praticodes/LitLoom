"""This file contains all the functions that help us use linear programming techniques to find
the optimal reading list for a book club.
"""

from pulp import LpMaximize, LpProblem, LpVariable
from books import Book, create_books_from_csv, sort_books_by_combined_score


def get_recommendations_lpp(book_list: list[Book], genre_votes: dict[str: int], num_books=10) -> list[Book]:
    """
    Solves a linear programming problem to return a list of reccomended books.
    >>> books = create_books_from_csv()
    >>> votes = {'Fiction': 4, 'Romance': 3, 'Feminism': 2, 'Horror': 1}
    >>> reccomendations_lpp = get_recommendations_lpp(books, votes)
    >>> lst = [reccomendations_lpp[i].title for i in range(0, 9)]
    >>> lst
    ['Lessons in Chemistry', 'Part of Your World', 'House of Sky and Breath', 'Reminders of Him', 'A Court of Silver Flames', 'Rule of Wolves', 'Chain of Iron', 'Better than the Movies', 'A Shadow in the Ember']
    """
    model = LpProblem("Best_Books_Selection", LpMaximize)
    book_vars = LpVariable.dicts("Book", book_list, cat="Binary")

    total_score = sum(book.get_combined_score(genre_votes) * book_vars[book] for book in book_list)
    model += total_score, "Total_Score_Objective"
    model += sum(book_vars[book] for book in book_list) == num_books, "Select_Num_Books"

    books_with_high_ratings = [book for book in book_list if book.rating > 4]
    warm_start_books = books_with_high_ratings[:num_books]
    for book in warm_start_books:
        book_vars[book].setInitialValue(1)

    model.solve()

    selected_books = [book for book in book_list if book_vars[book].value() == 1]
    return selected_books


def get_recommendations_sort(book_list: list[Book], genre_votes: dict[str: int], num_books=10) -> list[Book]:
    """
    Sorts book options to return a list of reccomended books
    >>> books = create_books_from_csv()
    >>> votes = {'Fiction': 4, 'Romance': 3, 'Feminism': 2, 'Horror': 1}
    >>> reccomendations = get_recommendations_sort(books, votes)
    >>> titles = [reccomendations[i].title for i in range(0, len(reccomendations))]
    >>> titles
    ['The Spanish Love Deception', 'Lessons in Chemistry', 'House of Sky and Breath', 'A Court of Silver Flames', 'A Shadow in the Ember', 'Reminders of Him', 'Rule of Wolves', 'Legendborn', 'Part of Your World', 'Chain of Iron']
    """
    sort_books_by_combined_score(book_list, genre_votes)
    return [book_list[-i] for i in range(0, num_books)]


def get_recommendations(selected_genres: list[str]) -> list[str]:
    """Return a list of books and their information based on the faster LPP algorithm.
    >>> get_recommendations(['Romance', 'Feminism'])
    ["'Lessons in Chemistry' by Bonnie Garmus", "'Part of Your World' by Abby Jimenez", "'House of Sky and Breath' by Sarah J. Maas", "'Reminders of Him' by Colleen Hoover", "'Heartstopper: Volume Four' by Alice Oseman", "'A Court of Silver Flames' by Sarah J. Maas", "'Rule of Wolves' by Leigh Bardugo", "'Chain of Iron' by Cassandra Clare", "'A Shadow in the Ember' by Jennifer L. Armentrout"]
    """
    books = create_books_from_csv()
    genres_dict = {selected_genre: 1 for selected_genre in selected_genres}
    recommendations = get_recommendations_lpp(books, genres_dict)
    refined = [f"'{recommendations[i].title}' by {recommendations[i].author}" for i in range(0, 9)]
    return refined


# TODO: Get metrics for improvement by switching to LPP.
# TODO: Create user system for submitting genre votes.
# TODO: Create UI for the application.
