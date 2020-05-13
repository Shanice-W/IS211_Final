Blog posting web application is built in Flask, Database is designed in sqlite3 using Python SQLAlchemy toolkit for Object Relational Mapping.
Login implementation is done using Flask Login library.
Database has 2 models User and Blogpost.

User model has 4 attributes, this entity stores following data :
id (user's Id)
username (User's Identity)
email (User's email)
password (User's password)

Blogpost model has 6 attributes:
id (id of the blogpost)
title (title of the blogpost)
date_posted (published date of the post)
author (author that published the post)
content (Post's Content)
poster_id (Author's Id, This field is a foreign Key of User Model)

Fuctions of web app
-login
-signup
-logout
-view posts (Posts are displayed on welcome page)
-add a Post (login required)
-delete a post ( login required)
-edit post (login required)

Pages in Web Application

-index.html (Welcome Page)
-dashboard.html (User Dashboard Page)
-edit.html (Post Edit Page)
-post.html (Page for View the selected post)
-login.html (Login Page)
-signup.html (Signup Page)

Tools used to develop blog app
-Python 3.6
-Atom IDE
-Sqlite3
-Venv Python Virtual Environment
