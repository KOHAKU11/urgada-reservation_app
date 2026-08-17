Table Reservation Management System

A simple Django-based Table Reservation Management System connected to a MySQL database through Laragon.

Technologies

Python

Django

MySQL

Laragon

HTML / CSS

Bootstrap

Django Admin

Project Modules

Customers

Table Categories

Tables

Reservations

Reservation Status

Payments

Audit Logs

Dashboard

Django Admin

Functional Requirements

The system is designed to support:

Creating customers

Allowing one customer to have multiple reservations

Creating table categories with multiple tables

Assigning tables to categories

Associating reservations with one customer and one table

Assigning valid reservation statuses

Recording reservation date, start time, end time, and guest count

Rejecting invalid guest counts

Rejecting an end time earlier than or equal to the start time

Rejecting reservations that exceed table capacity

Associating payments with reservations

Recording payment status

Generating audit-log records for important reservation activities

Creating records through Django forms

Retrieving records through views

Updating records

Deleting or cancelling records where appropriate

Using named URLs for implemented views

Project Structure

DjangoTableReservation/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── reservation_app/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── templates/
│   └── reservation_app/
└── static/
    └── reservation_app/

Installation

1. Open the project

cd C:\DjangoTableReservation

2. Activate the virtual environment

venv\Scripts\activate

3. Install Django

pip install django

Install the MySQL driver required by the project's database configuration if it is not already installed.

Laragon / MySQL Setup

Open Laragon.

Start MySQL.

Create the database configured in config/settings.py.

Make sure the database name, username, password, host, and port match the Django settings.

Example:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "table_reservation_db",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}

Use the actual MySQL port configured by Laragon.

Migrations

Run:

python manage.py makemigrations
python manage.py migrate

Check the project:

python manage.py check

A successful check should show:

System check identified no issues (0 silenced).

Create a Superuser

Create the administrator account:

python manage.py createsuperuser

Then enter the requested username, email, and password.

Run the System

python manage.py runserver

Main application:

http://127.0.0.1:8000/

Django Admin:

http://127.0.0.1:8000/admin/

Django Admin

The Django Admin interface is used for administrator-level database management.

The application can register:

Customers

Table Categories

Tables

Reservation Status

Reservations

Payments

Audit Logs

Reservation Validation

A reservation should only be saved when all required rules are satisfied.

Guest count

The guest count must be at least 1.

Guests = 0
→ Invalid

Time

The end time must be later than the start time.

Start: 6:00 PM
End:   6:00 PM
→ Invalid

Start: 8:00 PM
End:   6:00 PM
→ Invalid

Table capacity

The number of guests must not exceed the selected table's capacity.

Table capacity: 4
Guests: 6
→ Invalid

Reservation Relationship

The main relationships are:

Customer
   │
   └──< Reservations >── Table
                              │
                              └── Table Category

Reservation
   ├── Reservation Status
   ├── Payment
   └── Audit Logs

This supports the required customer, table, reservation, status, payment, and audit-log relationships.

Testing Checklist

Customers

Create a customer

View a customer

Update a customer

Delete a customer

Create multiple reservations for one customer

Tables

Create a table category

Create multiple tables in a category

Assign a table to a category

Update a table

Delete a table where appropriate

Reservations

Create a valid reservation

Select a customer

Select a table

Select a valid status

Record date and time

Record guest count

Reject invalid guest count

Reject invalid start/end time

Reject guests above table capacity

Update a reservation

Cancel a reservation

Payments

Create a payment

Associate it with a reservation

Record payment status

Update payment information

Audit Logs

Record important reservation activities

Verify audit records after create/update/cancel operations

Django Forms and Views

Create records through Django forms

Retrieve records through views

Update records

Delete/cancel where appropriate

Give every implemented view a named URL

Common Commands

python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test

Purpose

This project is intended as an educational/academic Table Reservation Management System. It demonstrates Django models, relationships, forms, views, validation, CRUD operations, authentication, MySQL database integration, and audit logging.
