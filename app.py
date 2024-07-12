from flask import Flask, jsonify, request
import json

app = Flask(__name__)

with open('books.json', 'r') as fileobj:
    books = json.load(fileobj)


def sync_books(books):
    updated_books = json.dumps(books)
    with open('books.json', 'w') as fileobj:
        fileobj.write(updated_books)


def validate_book_data(data):
    if "title" not in data or "author" not in data:
        return False
    return True


@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        # Get the new book data from the client
        new_book = request.get_json()

        if not validate_book_data(new_book):
            return jsonify({"error": "Invalid book data"}), 400

        # Generate a new ID for the book
        new_id = max(book['id'] for book in books) + 1
        new_book['id'] = new_id

        # Add the new book to our list
        books.append(new_book)

        # Write to file
        sync_books(books)

        # Return the new book data to the client
        return jsonify(new_book), 201
    else:
        # Handle the GET request
        return jsonify(books)


def find_book_by_id(book_id):
    """ Find the book with the id `book_id`.
    If there is no book with this id, return None. """
    for book in books:
        if book['id'] == book_id:
            return book
        return None


def update_a_book(updated_book):
    """ Finds the book with the id `book_id`.
       And replaces it in the json file """
    for i, book in enumerate(books):
        if book['id'] == updated_book['id']:
            books[i] = updated_book


@app.route('/api/books/<int:id>', methods=['PUT'])
def handle_book(id):
    # Find the book with the given ID
    book = find_book_by_id(id)

    # If the book wasn't found, return a 404 error
    if book is None:
        return '', 404

    # Update the book with the new data
    new_data = request.get_json()
    book.update(new_data)

    # Replace in JSON
    update_a_book(book)

    # Return the updated book
    return jsonify(book), 201


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    # Find the book with the given ID
    book = find_book_by_id(id)

    # If the book wasn't found, return a 404 error
    if book is None:
        return '', 404

    # Remove the book from the list
    books.remove(book)

    # Write to file
    sync_books(books)

    # Return the deleted book
    return jsonify(book), 201


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
