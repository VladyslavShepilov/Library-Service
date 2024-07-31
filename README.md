# Library Service API
A comprehensive service for renting books, equipped with notifications, payment processing, and extensive custom functionalities.
The project is organized into several modules to ensure scalability and maintainability


## Features
### Borrowing Functionality
* Track book prices and auto-update based on rental duration.
* Manage borrowing periods and overdue penalties.
### Notification Service
* Integrated with TelegramAPI for instant user notifications.
* Notifications for due dates, overdue reminders, and promotional messages.
### Payment Processing
* Integrated with Stripe for secure and efficient payment handling.
* Support for multiple payment methods and transaction tracking.
### Book Database
* Extensive catalog of books with detailed metadata.
* Track individual book instances for availability and condition.
### Admin Interface
* Enhanced admin functionalities accessible through a custom backend interface.
* Advanced filtering, sorting, and searching capabilities for efficient management.
### User Management
* Custom user model with email authentication for secure access.
* Role-based access control with extended functionalities for admin users.
### Admin Interface
* Enhanced admin functionalities accessible through a custom backend interface.
* Advanced filtering, sorting, and searching capabilities for efficient management.
### Django Admin Panel
* Customized admin panel for a seamless administrative experience.
* Manage users, books, borrowings, payments, and notifications.
### Security
* JWT authentication for secure API access.
* Comprehensive user permissions and access controls.

## How to run
Create a virtual environment

    python3 -m venv venv
    source venv/bin/activate

Install dependencies

    pip install -r requirements.txt

Run migrations

    python manage.py makemigrations
    python manage.py migrate

Create a superuser

    python manage.py createsuperuser

Start the server

    python manage.py runserver


Take tokens from:

    "/user/token/"
    "user/ token/refresh/"
    "user/ token/verify/"
    

## Screenshots:
![Books List](Demo/books.png)

![Borrowings List](Demo/borrowings.png)

![Filtering feature on multiple pages](Demo/borrowings_det.png)

![Different info, depending on request type](Demo/payment.png)
