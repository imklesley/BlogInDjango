# SnakeBlog

SnakeBlog is an application created with Django and Django Rest Framework that allows users to Create, Update, Read and Delete their blog posts. It also allows users to Login and Register to the application. This application can be used as an API for other applications using techs such as Flutter, VueJS, etc. 


## Features
* User authentication (Login and Register)
* CRUD operations on blog posts (Create, Read, Update, Delete)
* Access control (only authenticated users can create, update, and delete their posts)
* Pagination for blog posts

## Prerequisites

Before you can use SnakeBlog you need to have the following packages installed:

* Python 3.x
* Django 
* Django Rest Framework

## Installation

* Clone the repository:

```
git clone https://github.com/imklesley/snakeblog-django.git
```

* Install the requirements:

```
pip install -r requirements.txt
```

* Apply the migrations:

```
python manage.py migrate
```

* Create a superuser:

```
python manage.py createsuperuser
```

* Run the server:

```
python manage.py runserver
```

## Usage

Once the server is running you can access the API endpoints at http://localhost:8000/api/

## API Endpoints

### Authentication
Use this example of endpoint:
`ADDRESS:PORT/api/account/ENDPOINT`

**Register**

* `POST /register` - This endpoint allows a user to register a new account.

**Login**

* `POST /login` - This endpoint allows a user to login and receive an authentication token.

**My Account**

* `GET /my_account` - This endpoint allows a logged in user to view their account information.

**Update Account**

* `PUT /update_account` -
This endpoint allows a logged in user to update their account information.

### Posts
Use this example of endpoint:

`ADDRESS:PORT/api/blog/ENDPOINT`

This endpoint allows users to Create, Update, Read and Delete their posts.

* `GET` `/<slug:slug>/` - Retrieve a single blog post with the given slug.

* `PUT` `/<slug:slug>/update` - Update the blog post with the given slug.

* `DELETE` `/<slug:slug>/delete` - Delete the blog post with the given slug.

* `POST` `/create` - Create a new blog post.

* `GET` `/my-posts` - Retrieve all blog posts created by the current user.

* `GET` `/list-by-classview` - Retrieve all blog posts using a class-based view.

* `GET` `/list` - Retrieve all blog posts.





<br>

##

<p align="center">Developed by <span color="#007DFF" >Klesley Gonçalves</span></p>