import pulp


def recommend_books(dataset, max_total_time):
    # Create a binary variable for each book
    books = range(len(dataset))
    x = pulp.LpVariable.dicts('book', books, lowBound=0, upBound=1, cat=pulp.LpInteger)

    # Create a linear programming problem
    prob = pulp.LpProblem('BookRecommendation', pulp.LpMaximize)

    # Objective: Maximize the sum of average ratings and number of reviews
    prob += sum((dataset[i]['avg_rating'] + dataset[i]['num_reviews']) * x[i] for i in books), 'Total_Score'

    # Constraint: Total time to read
    prob += sum(dataset[i]['time_to_read'] * x[i] for i in books) <= max_total_time, 'Time_Constraint'

    # Solve the linear programming problem
    prob.solve()

    # Extract recommended books
    recommended_books = [dataset[i] for i in books if pulp.value(x[i]) == 1]

    return recommended_books


# Example dataset (replace with your actual dataset)
dataset = [
    {
        'title': 'The Mystery of the Hidden Key',
        'avg_rating': 4.5,
        'num_reviews': 150,
        'time_to_read': 3
    },
    {
        'title': 'Fantasy Realm Chronicles',
        'avg_rating': 4.8,
        'num_reviews': 230,
        'time_to_read': 4
    },
    {
        'title': 'Science Adventure Explorers',
        'avg_rating': 4.3,
        'num_reviews': 180,
        'time_to_read': 3
    },
    {
        'title': 'Heartfelt Romance Journey',
        'avg_rating': 4.6,
        'num_reviews': 120,
        'time_to_read': 2
    },
    {
        'title': 'Thrills and Chills',
        'avg_rating': 4.7,
        'num_reviews': 200,
        'time_to_read': 3
    },
    # Add more books to the dataset
]

max_total_time = 15

recommended_books = recommend_books(dataset, max_total_time)
for book in recommended_books:
    print(f"Title: {book['title']}, Avg Rating: {book['avg_rating']}, Num Reviews: {book['num_reviews']}")
