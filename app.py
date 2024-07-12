from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/api/books', methods=['GET'])
def get_books():
    books = [
        {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"id": 2, "title": "1984", "author": "George Orwell"}
    ]
    return jsonify(books)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)