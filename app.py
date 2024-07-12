from flask import Flask, jsonify, request
import json

app = Flask(__name__)

with open('books.json', 'r') as fileobj:
    books = json.load(fileobj)

def sync_books(books):
    updated_books = json.dumps(books)
    with open('books.json', 'w') as fileobj:
        fileobj.write(updated_books)

@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        # Get the new book data from the client
        new_book = request.get_json()

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)