from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


books = [
{"id": 1, "title": "1984", "author": "George Orwell" },
{"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]


@app.route('/books', methods=['GET'])
def get_books():
    """Return a list of all the books"""
    return jsonify(books)


@app.route('/books', methods=['POST'])
def add_book():
    """Adds a book"""
    if not request.json or 'title' not in request.json or 'author' not in request.json:
        return jsonify({'error': 'Bad Request'}), 400
    new_book = {
        'id': books[-1]['id'] + 1 if books else 1,
        'title': request.json['title'],
        'author': request.json['author']
    }

    books.append(new_book)
    return jsonify(new_book), 201



@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Return a book by its book_id"""
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(book)


if __name__ == '__main__':
    app.run(debug=True)