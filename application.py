import os

from flask import Flask, session, render_template, request, jsonify, redirect, url_for, Response, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import string
import requests
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):

    def __init__(self,id):
        self.id = id
        self.username = 'username'
        self.password = 'password'
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.username, self.password)



@app.route("/")
#@login_required
def index():
    #return render_template("register.html")
    return render_template("main.html")
    #return render_template("sign_in.html")

@app.route("/reg")
def reg():
    return render_template("register.html")
    #return render_template("sign_in.html")

@app.route("/login")
def login():
    #return render_template("register.html")
    return render_template("sign_in.html")

@app.route("/register", methods=["POST"])
def register():
    """RIGISTER HERE"""
    username= request.form.get("input_username")
    email= request.form.get("input_email")
    password= request.form.get("input_password")
    confirm_password= request.form.get("confirm_input_password")
    if username == "" or password == "" or email == "" or confirm_password == "": return render_template("error.html", message="Please fill out the fields")

    #Make sure the user is not already registered:
    if password != confirm_password : return render_template("error.html", message="Passwords dont match!")

    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
        db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
            {"username": username, "email": email,"password": password})
    else:
        return render_template("error.html", message="Username Already Exists")    
    db.commit()

    return redirect(url_for('login'))

@app.route("/success")
#@login_required
def success():
    return "Registration Successful!!"

@app.route("/sign_in",methods=["POST"])
def sign_in():
    username= request.form.get("input_username")
    password= request.form.get("input_password")

    if username == "" or password == "" : return render_template("error.html", message="Please fill out the fields")

    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
        return render_template("error.html", message="User not registered")
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 1:
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        userid = user.id
        user = User(userid)
        login_user(user)
        return redirect(url_for('index'))
        #return render_template("main.html")
    else: return render_template("error.html", message="Invalid Password")

@app.route("/search",methods=["POST"])
#@login_required
def search():
    search_by = request.form.get("search_by")
    search_input = request.form.get("search_input")
    search_input_capital = search_input.capitalize()
    search_input_lower = search_input.lower()

    if search_by == 'select_isbn':
        search_result = db.execute(f"SELECT * FROM books WHERE isbn LIKE '%{search_input}%' OR isbn LIKE '%{search_input_capital}%' OR isbn LIKE '%{search_input_lower}%' ").fetchall()
        if search_result == None:
            message = "No books found"
        else: message = f"Found {len(search_result)} books"
        return render_template("search_result.html", search_result=search_result,message=message)

    if search_by == 'select_title':
        search_result = db.execute(f"SELECT * FROM books WHERE title LIKE '%{search_input}%' OR title LIKE '%{search_input_capital}%' OR title LIKE '%{search_input_lower}%' ").fetchall()
        if search_result == None:
            message = "No books found"
        else: message = f"Found {len(search_result)} books"
        return render_template("search_result.html", search_result=search_result,message=message)
    
    if search_by == 'select_author':
        search_result = db.execute(f"SELECT * FROM books WHERE author LIKE '%{search_input}%' OR author LIKE '%{search_input_capital}%' OR author LIKE '%{search_input_lower}%' ").fetchall()
        if search_result == None:
            message = "No books found"
        else: message = f"Found {len(search_result)} books"
        return render_template("search_result.html", search_result=search_result,message=message)    
    
    if search_by == 'select_any':
        search_result = []
        isbn_result = db.execute(f"SELECT * FROM books WHERE isbn LIKE '%{search_input}%' OR isbn LIKE '%{search_input_capital}%' OR isbn LIKE '%{search_input_lower}%' ").fetchall()
        for result in isbn_result:
            search_result.append(result)
        title_result = db.execute(f"SELECT * FROM books WHERE title LIKE '%{search_input}%' OR title LIKE '%{search_input_capital}%' OR title LIKE '%{search_input_lower}%' ").fetchall()       
        for result in title_result:
            search_result.append(result)
        author_result = db.execute(f"SELECT * FROM books WHERE author LIKE '%{search_input}%' OR author LIKE '%{search_input_capital}%' OR author LIKE '%{search_input_lower}%' ").fetchall()        
        for result in author_result:
            search_result.append(result)
        
        if search_result == None:
            message = "No books found"
        else: message = f"Found {len(search_result)} books"
        return render_template("search_result.html", search_result=search_result,message=message)

@app.route("/book/<int:book_id>")
#@login_required
def book(book_id):
    try:
        book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
        #print("All good until here")
        isbn = book.isbn
        try:
            reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
            #print("All good until here")

        except: 
            reviews = "No reviews yet"
        try:
            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "CbrhM9CbXo0tgNEgjQtFAg", "isbns": isbn})
            info = res.json()
            #print("All good until here")

        except:
            info['books'][0]['average_rating'] = "Data Not available!"
            info['books'][0]['work_ratings_count'] = "Data Not available!"
        
        #print("All good until here")

        return render_template("book.html", book = book, info = info, reviews = reviews)

    except: 
        return render_template("error.html", message="Book not in our records!")


#Our own API:
@app.route("/api/<string:isbn>")
def flight_api(isbn):
    """Return details about a single book."""
    try:
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "CbrhM9CbXo0tgNEgjQtFAg", "isbns": isbn})
        info = res.json()
        return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": info['books'][0]['work_ratings_count'],
            "average_score": info['books'][0]['average_rating']
        })
    except:
        return jsonify({"error": "Invalid ISBN"}), 404


@app.route("/review", methods=["POST"])
#@login_required
def review():
    review = request.form.get("input_review")
    rating = request.form.get("rating")
    username = request.form.get("input_username")
    isbn = request.form.get("input_isbn")         

    if db.execute("SELECT * FROM reviews WHERE username = :username AND isbn = :isbn", {"username": username, "isbn": isbn}).rowcount == 0:
        db.execute("INSERT INTO reviews (isbn, username, review, rating) VALUES (:isbn, :username, :review, :rating)",
            {"isbn": isbn, "username": username, "review": review,"rating": rating})
    else:
        return render_template("error.html", message="You have already reviewed the book")    
    db.commit()


    return render_template("test.html", review = review, rating = rating, username = username, isbn = isbn)

@app.route("/prelogout")
def prelogout():
    return redirect(url_for('logout'))

@app.route("/logout")
#@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

# callback to reload the user object        
@login_manager.user_loader
def load_user(id):
    return User(id)


if __name__ == '__main__':
    app.run(debug=True)