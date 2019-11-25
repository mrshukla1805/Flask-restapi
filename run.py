from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty

class BookSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/book', methods=['POST'])
def add_book():
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  new_book = book(name, description, price, qty)

  db.session.add(new_book)
  db.session.commit()

  return book_schema.jsonify(new_book)


@app.route('/book', methods=['GET'])
def get_books():
  all_books = book.query.all()
  result = books_schema.dump(all_books)
  return jsonify(result.data)


@app.route('/book/<id>', methods=['GET'])
def get_book(id):
  book = book.query.get(id)
  return book_schema.jsonify(book)


@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
  book = book.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  book.name = name
  book.description = description
  book.price = price
  book.qty = qty

  db.session.commit()

  return book_schema.jsonify(book)


@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
  book = book.query.get(id)
  db.session.delete(book)
  db.session.commit()

  return book_schema.jsonify(book)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)