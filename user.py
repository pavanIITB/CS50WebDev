import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    #db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, email VARCHAR NOT NULL, password VARCHAR NOT NULL)")
    #print("Created users table")
    users= db.execute("SELECT * FROM users").fetchall()
    if users == None:
        print("No users yet!")
        return
    for username, email, password in users:
        print(f"Username: {username} \t Email: {email} \t Password: {password}")
    db.commit()

if __name__ == "__main__":
    main()
