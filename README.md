# Flask Bucketlist API

[![Build Status](https://travis-ci.org/andela-austinroy/cp2-flask-bucketlist-api.svg?branch=develop)](https://travis-ci.org/andela-austinroy/cp2-flask-bucketlist-api) [![Code Health](https://landscape.io/github/andela-austinroy/cp2-flask-bucketlist-api/develop/landscape.svg?style=flat)](https://landscape.io/github/andela-austinroy/cp2-flask-bucketlist-api/develop) [![license](https://img.shields.io/github/license/andela-austinroy/cp2-flask-bucketlist-api.svg)]() [![Coverage Status](https://coveralls.io/repos/github/andela-austinroy/cp2-flask-bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/andela-austinroy/cp2-flask-bucketlist-api?branch=develop)

Checkpoint 2 project on creating a RESTful bucketlist API using python flask. This project makes use of the Flask framework to execute a RESTful API that allows users to create edit and save bucketlists on a database. Response data is in json format.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Python 2.7
Comes inbuilt for unix but can also be downloaded from

```
https://www.python.org/downloads/
```

### Installing

Clone this repo from github by running:

```
$ git clone git@github.com:andela-austinroy/cp2-flask-bucketlist-api.git
```

Set up a virtual environment for the project and install the dependencies

```
$ mkvirtualenv amity
$ pip install -r requirements.txt
```
### Running the project locally
Start the local server

```
$ python manage.py runserver
```

Once the server is running the API is accessible on localhost and uses port 5000.

#### URL endpoints

The following endpoints are provided 

|URL Endpoint| HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `/auth/register/` | `POST`  | Register a new user|
|  `/auth/login/` | `POST` | Login and retrieve token|
| `/bucketlists/` | `POST` | Create a new Bucketlist |
| `/bucketlists/` | `GET` | Retrieve all bucketlists for user |
| `/bucketlists/?limit=2` | `GET` | Retrieve one bucketlist per page |
| `/bucketlists/?q=bl` | `GET` | Match bucketlist by name |
| `/bucketlists/<id>/` | `GET` |  Retrieve bucket list details |
| `/bucketlists/<id>/` | `PUT` | Update bucket list details |
| `/bucketlists/<id>/` | `DELETE` | Delete a bucket list |
| `/bucketlists/<id>/items/` | `POST` |  Create items in a bucket list |
| `/bucketlists/<id>/items/<item_id>/` | `DELETE`| Delete a item in a bucket list|
| `/bucketlists/<id>/items/<item_id>/` | `PUT`| update a bucket list item details|



## Running the tests

Tests are done using python nosetests. They can be run by the command

```
nosetests --rednose -v --with-coverage --cover-package=app
```
This command also provides test coverage results.

The tests make use of HTTP response codes to ensure users are getting the expected responses from the api as well as token based authentication which ensures security of users data by ensuring only authorised users gain access to sensitive data.


## Built With

* [Python](http://www.python.org) - A verstile programming language
* [Flask](http://flask.pocoo.org/) - A multipurpose python web framework

## Contributing

Contributions are open, fork the repository and make a pull requestwith the changes which will be reviewed before merging on approval.

## Authors

* **Austin Roy** - *Initial work* - [Austin Roy](https://github.com/andela-austinroy)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Several Andela Fellows consulted during development
* Facilitators

