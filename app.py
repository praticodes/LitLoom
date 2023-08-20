import time
from flask import Flask, render_template, request, redirect, url_for
from lpp import get_recommendations

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home_page.html')


@app.route('/select_genres')
def select_genres():
    return render_template('genre_requests.html')


@app.route('/process', methods=['POST'])
def process():
    selected_genres = request.form.getlist('genres')
    form_submitted = request.form.get('form_submitted')
    show_loading_overlay = True

    if form_submitted == 'true':
        # Simulate processing time
        time.sleep(0.5)
        books = get_recommendations(selected_genres)
        time.sleep(0.5)
        return redirect(url_for('display_selected_genres', books=books))

    return render_template('genre_requests.html', show_loading_overlay=show_loading_overlay)


@app.route('/display_selected_genres')
def display_selected_genres():
    books = request.args.getlist('books')
    return render_template('selected_genres_page.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
