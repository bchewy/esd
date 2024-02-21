from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import os
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:root@localhost:3306/book"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

db = SQLAlchemy(app)

CORS(app)


class Book(db.Model):
    __tablename__ = "book"

    isbn13 = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    availability = db.Column(db.Integer)

    def __init__(self, isbn13, title, price, availability):
        self.isbn13 = isbn13
        self.title = title
        self.price = price
        self.availability = availability

    def json(self):
        return {
            "isbn13": self.isbn13,
            "title": self.title,
            "price": self.price,
            "availability": self.availability,
        }


@app.route("/book")
def get_all():
    booklist = db.session.scalars(db.select(Book)).all()

    if len(booklist):
        return jsonify(
            {"code": 200, "data": {"books": [book.json() for book in booklist]}}
        )
    return jsonify({"code": 404, "message": "There are no books."}), 404


@app.route("/book/<string:isbn13>")
def find_by_isbn13(isbn13):
    book = db.session.scalars(db.select(Book).filter_by(isbn13=isbn13).limit(1)).first()

    if book:
        return jsonify({"code": 200, "data": book.json()})
    return jsonify({"code": 404, "message": "Book not found."}), 404


@app.route("/book/<string:isbn13>", methods=["POST"])
def create_book(isbn13):
    book = db.session.scalars(db.select(Book).filter_by(isbn13=isbn13).limit(1)).first()

    if book:
        return jsonify(
            {"code": 400, "data": {"isbn13": isbn13}, "message": "Book already exists."}
        ), 400

    data = request.get_json()
    book = Book(isbn13, **data)

    try:
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = (
            str(e)
            + " at "
            + str(exc_type)
            + ": "
            + fname
            + ": line "
            + str(exc_tb.tb_lineno)
        )
        print(ex_str)

        return jsonify(
            {
                "code": 500,
                "data": {"isbn13": isbn13},
                "message": "An error occurred creating the book. " + ex_str,
            }
        ), 500

    return jsonify({"code": 201, "data": book.json()}), 201


@app.route("/book/<string:isbn13>", methods=["PUT"])
def update_book(isbn13):
    book = db.session.scalars(db.select(Book).filter_by(isbn13=isbn13).limit(1)).first()

    if not book:
        return jsonify(
            {"code": 404, "data": {"isbn13": isbn13}, "message": "Book not found."}
        ), 400

    data = request.get_json()

    try:
        if "title" in data:
            book.title = data["title"]
        if "price" in data:
            book.price = data["price"]
        if "availability" in data:
            book.availability = data["availability"]
        db.session.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = (
            str(e)
            + " at "
            + str(exc_type)
            + ": "
            + fname
            + ": line "
            + str(exc_tb.tb_lineno)
        )
        print(ex_str)

        data["isbn13"] = isbn13
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An unexpected error occurred updating the book. " + ex_str,
            }
        ), 500

    return jsonify({"code": 201, "data": book.json()}), 201


@app.route("/book/<string:isbn13>", methods=["DELETE"])
def delete_book(isbn13):
    book = db.session.scalars(db.select(Book).filter_by(isbn13=isbn13).limit(1)).first()

    if not book:
        return jsonify(
            {"code": 404, "data": {"isbn13": isbn13}, "message": "Book not found."}
        ), 400

    # else
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = (
            str(e)
            + " at "
            + str(exc_type)
            + ": "
            + fname
            + ": line "
            + str(exc_tb.tb_lineno)
        )
        print(ex_str)

        return jsonify(
            {
                "code": 500,
                "data": {"isbn13": isbn13},
                "message": "An unexpected error occurred deleting the book. " + ex_str,
            }
        ), 500

    return jsonify({"code": 201, "isbn13": isbn13}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
