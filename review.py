import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    #db.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, username VARCHAR NOT NULL, review VARCHAR NOT NULL, rating INTEGER NOT NULL)")
    #print("Created reviews table")
    reviews= db.execute("SELECT * FROM reviews").fetchall()
    if reviews == None:
        print("No reviews yet!")
        return
    for isbn, username, review, rating in reviews:
        print(f"ISBN: {isbn} \t Username: {username} \t review: {review} \t rating: {rating}")
    db.commit()

if __name__ == "__main__":
    main()
