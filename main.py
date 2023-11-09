import sqlite3
from flask import Flask, jsonify, request, g

DATABASE = 'library.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/books', methods=['GET'])
def get_books():
    """Get a list of all books."""
    rows = query_db('SELECT * FROM books')
    books = [dict(row) for row in rows]
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    """Add a new book."""
    if not request.json or 'title' not in request.json or 'author' not in request.json:
        return jsonify({'error': 'Bad Request'}), 400
    db = get_db()
    db.execute('INSERT INTO books (title, author) VALUES (?, ?)',
               [request.json['title'], request.json['author']])
    db.commit()
    return jsonify({'success': 'Book added'}), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a book by its ID."""
    book = query_db('SELECT * FROM books WHERE id = ?', [book_id], one=True)
    if book is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(dict(book))

if __name__ == '__main__':
    #init_db()  # Make sure to initialize the database the first time you run the application
    app.run(debug=True)
