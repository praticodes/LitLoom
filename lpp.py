import pulp

# List of books and their attributes (enjoyment, rating, price, duration, award-winning, trending, best-selling,
# representation)

# should create representation score based on user backgrounds.

books = [
    {"title": "Book A", "enjoyment": [8, 9, 7, 8], "rating": 4.2, "price": 20, "duration": 4, "award_winning": True, "trending": False, "best_selling": False, "representation": "Black"},
    {"title": "Book B", "enjoyment": [10, 8, 9, 7], "rating": 4.7, "price": 30, "duration": 5, "award_winning": True, "trending": True, "best_selling": True, "representation": "LGBT"},
    {"title": "Book C", "enjoyment": [7, 9, 8, 6], "rating": 4.5, "price": 25, "duration": 3, "award_winning": False, "trending": True, "best_selling": False, "representation": "South Asian"},
    # Add more books here
]

# objective function: 5 enjoyment + 5 rating + 2.5 price + 1 duration + 3 award-winning + 2 trending + 2 best-selling.
# no one should have read the book before.

# User's budget and maximum reading duration
budget = 100
max_duration = 15

# Create a PuLP problem instance
problem = pulp.LpProblem("BookListOptimization", pulp.LpMaximize)

# Binary decision variables for each book
book_vars = {book["title"]: pulp.LpVariable(book["title"], 0, 1, pulp.LpBinary) for book in books}

# Total enjoyment objective function for each person
enjoyment_scores = [[] for _ in range(4)]
for book in books:
    for i in range(4):
        enjoyment_scores[i].append(book["enjoyment"][i] * book_vars[book["title"]])

for i in range(4):
    problem += pulp.lpSum(enjoyment_scores[i]) >= 10  # Minimum enjoyment score for each person

# Total enjoyment score objective function (sum of all persons' scores)
total_enjoyment = [pulp.lpSum(enjoyment_scores[i]) for i in range(4)]
problem += pulp.lpSum(total_enjoyment)

# Constraint: Select only one book
problem += pulp.lpSum([book_vars[book["title"]] for book in books]) == 1

# Constraints to minimize price and reading duration
problem += pulp.lpSum([book["price"] * book_vars[book["title"]] for book in books]) <= budget
problem += pulp.lpSum([book["duration"] * book_vars[book["title"]] for book in books]) <= max_duration

# Solve the problem
problem.solve()

# Print recommended book
print("Status:", pulp.LpStatus[problem.status])
for book in books:
    if book_vars[book["title"]].varValue > 0:
        print(f"Recommended Book: {book['title']} (Enj: {book['enjoyment']}, Rating: {book['rating']}, Price: ${book['price']}, Duration: {book['duration']}h)")
