# 2001-cw2
COMP2001 Coursework 2

This project is a Flask-based API for managing trails and users, with authentication integrated via an external API and SQL Server as the database backend. The API includes functionality to list and add trails and users, as well as access Swagger documentation for ease of use.

Features

Authentication: Verifies user credentials against an external authentication API.

Trail Management:

Get a list of all trails.

Add a new trail with trail name and length.

User Management:

Get a list of all users.

Add a new user by name.

API Documentation: Interactive API documentation available through Swagger UI.

Setup and Requirements

Prerequisites

Python 3.7+

Flask

requests for making HTTP requests.

pyodbc for database connectivity.

SQL Server with the required database and tables set up.

Installation

Clone the repository.

Install required dependencies:

pip install -r requirements.txt

Configure the database and authentication settings as required.

Configuration

Database

The application connects to a Microsoft SQL Server database using the pyodbc library. Connection details are configured in the DB_CONFIG dictionary:

DB_CONFIG = {
    "driver": "{ODBC Driver 17 for SQL Server}",
    "server": "localhost",
    "database": "COMP2001CW2",
    "username": "SA",
    "password": "C0mp2001!"
}

Update these values to match your SQL Server instance.

Authentication

The application uses an external API for authentication. The verify_credentials function sends the user's email and password to the API endpoint specified in auth_url:

auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

Replace this URL with the appropriate endpoint for your authentication service.

Running the Application

Ensure that the database and required tables are set up (see Database section below).

Start the Flask application:

python app.py

Access the Swagger documentation at: http://127.0.0.1:5000/swagger

API Endpoints

Authentication

POST /auth: Validates user credentials against the authentication API.

Trails

GET /trails: Retrieves all trails.

POST /trails: Adds a new trail. Requires TrailName and TrailLength in the JSON body.

Users

GET /users: Retrieves all users.

POST /users: Adds a new user. Requires UserName in the JSON body.

Swagger Documentation

Accessible at: /swagger
