from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Bootstrap5(app)

class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'

db =SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int]= mapped_column(Integer, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        pass

    ##READ ALL RECORDS
    # Construct a query to select from the database. Returns the rows in the database
    result = db.session.execute(db.select(Book).order_by(Book.title))
    # Use .scalars() to get the elements rather than entire rows from the database
    all_books = result.scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=['GET','POST'])
def add():
    if request.method=='POST':
        with app.app_context():
            new_book = Book(title= request.form['book_name'], author= request.form['book_author'], rating=request.form['book_rating'])
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for("home"))

    return render_template('add.html')


@app.route("/update/<int:index>", methods=['GET', 'POST'])
def update_book(index):

    if request.method == 'POST':
        book_to_update = db.session.execute(db.select(Book).where(Book.id == int(index))).scalar()
        book_to_update.rating = request.form['changed_rating']
        db.session.commit()
    result = db.session.execute(db.select(Book).where(Book.id==int(index)))
    selected_book = result.scalar()
    return render_template("edit_book.html", book=selected_book)


@app.route("/delete")
def delete_book():
    print(request.args.get('id'))
    book_id = int(request.args.get("id"))  # Get the ID from the request arguments
    db.session.execute(db.delete(Book).where(Book.id == book_id))
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

