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

    model += sum(book.get_combined_score(genre_votes) * book_vars[book] for book in book_list), "Total_Score_Objective"
    model += sum(book_vars[book] for book in book_list) == num_books, "Select_Num_Books"

    model.solve()

    top_books = [book for book in book_list if book_vars[book].value() == 1]
    return top_books
