# Project 1

Web Programming with Python and JavaScript
The file: application.py launches the page. 
review.py import.py and user.py are one-time-use files to create reviews, books and users tables respectively in the database.
testcode01.py file is a scratch file, used to test small snippets of the code before adding it to the application.py file

On startup(the '/' route), login page shows up. It also has a button to register.
If the username that is entered on login page is not registered, it prompts this in an error message.
If username is present but password is wrong, it also shows up the error message.
The sign_in.html page deals with this.

The register page also checks if the new input username already exists.
The register.html file deals with this.
It also has confirm password input, which prompts the user if the input password and confirm passwords dont match.

Once everything is well, user is authenticated and signed in, the search page shows up, which has a button to logout in the top
This is handled by the main.html file.
The search is very thoughtfully implemented. It gives a option to 'search by' to specify if the search query is a title, author or isbn
number. It also has a 'search by any' option in the drop down list which searches the keyword in all of the columns: title, author and isbn. Also note: we can search by the complete keyword or a part of the keyword!!!

Then we are directed to a search results page, which tells the number of search results are found. This is handled by search_result.html
Also we get a list of books, which are reference links to the respective page of book details and review submission.
The individual book page is rendered by book.html file
The review submission page takes rating and review by current user and also displays is other users' reviews of the book.
The current user can submit the review only once and if attempts to submit again, the error message shows up.
All the .html files in the template extend the layouts.html file.

For the purpose of user review input, I tried and added a feature of star ratings in html and css. It is implemented in the <style> part of the layouts file.