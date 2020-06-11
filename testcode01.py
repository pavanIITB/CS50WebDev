import requests
try:
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "CbrhM9CbXo0tgNEgjQtFAg", "isbns": "9732168146"})

    info = res.json()
    #print(info["books"][])


    print(info['books'][0]['work_ratings_count'])
    print(info['books'][0]['average_rating'])
except:
    print("Data not Available")