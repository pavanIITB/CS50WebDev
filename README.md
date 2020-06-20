# Project 2

Web Programming with Python and JavaScript

This is a simple Flask web application where users can enter giving a name, and then both create Chatrooms called Channels or go into one of the already existing (in case there is already one at least). 
Into a Channel, they can type and send messages which only exist into that Channel and other users can read them and respond.


**Application.py**

we have two dictionaries: one for users and other for channels.
The *connect* is the most important socket. It is ths very first socket to load, and it calls all other sockets mentioned below. The *new channel* takes the value new channel ad stores in the channels dictionary. The *new msg* socket takes any message emitted by any of the user and stores it in the key of that particular channel in the channel's dictionary. The *get channels* and *get messages* sockets are self explainatory, they emit the channels list, and the list of messages in the channel that is currently active


**Static**

Two files are present in the static folder. The index.js responsible for the entire socketIO and frontend functions.  Also the custom CSS stylesheet styles.css foe some custom styling although I have also included the bootstrap referene link.
*show channels* function grabs the ul that displays the channels list. Each of the list item when clicked, calls for *show_active_channel* function that highlights the channel that is clicked, and displays the messages in that channel by calling the function *show_msg*
The *get_username* function checks if the username is stored locally in the browser, if not, calls for the modal to query for the username.

**Templates**

This contain the file index.html, which has references to all the stylesheets and only the html code. All the javascript part is separately written in the index.js file in the static folder. 

**Personal Touch**

My personal touch in this project was to implement the option of attaching files along with the messages. for the outher users the file attachment appears as a link, clicking upon which the attachment is downloaded.