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
    return render_template("register.html")
    
@app.route("/register", methods=["POST"])
def register():
    """RIGISTER HERE"""
    username= request.form.get("input_username")
    email= request.form.get("input_email")
    password= request.form.get("input_password")
    
    #Make sure the user is not already registered:
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

if __name__ == '__main__':
    app.run(debug=True)