import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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


@app.route("/")
def index():
    #return render_template("register.html")
    return render_template("sign_in.html")

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

    return "Registration Successful!!"

@app.route("/success")
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
        return render_template("main.html")
    else: return render_template("error.html", message="Invalid Password")

@app.route("/search",methods=["POST"])
def search():
    search_by = request.form.get("search_by")
    search_input = request.form.get("search_input")

    if search_by == 'select_isbn':
        search_result = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": search_input}).fetchall()
        if search_result == None:
            message = "No books found"
        else: message = f"Found {len(search_result)} books"
        return render_template("search_result.html", search_result=search_result,message=message)

    if search_by == 'select_title':
        search_result = db.execute("SELECT * FROM books WHERE title = :title", {"title": search_input}).fetchall()
        if search_result == None:
            message = "No books found"
        else: message = f"Found {len(search_result)} books"
        return render_template("search_result.html", search_result=search_result,message=message)
    
    if search_by == 'select_author':
        search_result = db.execute("SELECT * FROM books WHERE author = :author", {"author": search_input}).fetchall()
        if search_result == None:
            message = "No books found"
        else: message = f"Found {len(search_result)} books"
        return render_template("search_result.html", search_result=search_result,message=message)    
    
    #search_any Incomplete
    if search_by == 'select_any':
        search_result = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": search_input}).fetchall()
        if search_result == None:
            message = "No books found"
        else: message = f"Found {len(search_result)} books"
        return render_template("search_result.html", search_result=search_result,message=message)

@app.route("/book/<int:book_id>")
def book(book_id):
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    return render_template("book.html", book = book)



if __name__ == '__main__':
    app.run(debug=True)