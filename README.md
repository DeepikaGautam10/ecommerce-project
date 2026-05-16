# 🕒 Watch House — Django E-Commerce Store

Watch House is a fully functional e-commerce web application for selling watches,
built with **Django** and **MySQL**. It has a modern, responsive **dark theme** and
covers everything a small online store needs: browsing products, searching and
filtering, a shopping cart, checkout, order history, user accounts, and a staff
area for managing products and categories.

This project was built as a **bachelor-level academic project** and is a good
starting point for learning how a real Django web application is structured.

---

## ✨ Features

- 🏠 **Home page** with featured products and category highlights
- 🛍️ **Shop page** with category filtering, keyword search, and pagination
- 🔎 **Product detail** pages with related products
- 🛒 **Shopping cart** — add, update quantity, and remove items
- 💳 **Checkout** with shipping details and multiple payment methods
- 📦 **Order history** — customers can view their past orders
- 👤 **User accounts** — sign up, log in, log out, and password reset
- 🔧 **Staff management area** — create, edit, and delete products & categories
- 📋 **Order management** — staff can view every order and update its status
  (Pending → Processing → Shipped → Delivered / Cancelled)
- 🎨 **Modern responsive dark UI** — mobile-first, built on Bootstrap 5
- ⚙️ **Django admin** for full back-office control

---

## 🧰 Tech Stack

| Layer     | Technology            |
|-----------|-----------------------|
| Backend   | Python, Django 5+     |
| Database  | MySQL                 |
| Frontend  | HTML, CSS, Bootstrap 5, JavaScript |
| Icons     | Font Awesome          |

---

## 📁 Project Structure

```
ecommerce_lab3/                  <-- Git repository root (this folder)
│   README.md
│   .gitignore
│
└── ecommerce_lab3/              <-- Django project folder (run commands here)
    │   manage.py
    │   requirements.txt
    │   load_sample_data.py      <-- script to add demo products
    │
    ├── ecommerce_project/       <-- project settings & URLs
    ├── accounts/                <-- users, login, signup, password reset
    ├── products/                <-- products, categories, cart
    ├── orders/                  <-- checkout and orders
    ├── templates/               <-- all HTML pages
    ├── static/                  <-- CSS, JavaScript, images
    └── media/                   <-- uploaded product/category images
```

> ⚠️ **Important:** all `python manage.py ...` commands must be run from the
> **inner** `ecommerce_lab3/` folder (the one that contains `manage.py`).

---

## 🚀 Getting Started (Beginner Guide)

Follow these steps to run the project on your own computer.

### 1. Prerequisites

Make sure you have these installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [MySQL Server 8+](https://dev.mysql.com/downloads/mysql/)
- [Git](https://git-scm.com/downloads)

### 2. Get the code

```bash
git clone <your-repository-url>
cd ecommerce_lab3/ecommerce_lab3
```

### 3. Create a virtual environment

A virtual environment keeps this project's packages separate from other projects.

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install the dependencies

```bash
pip install -r requirements.txt
```

### 5. Create the MySQL database

Open the MySQL command line (or MySQL Workbench) and run:

```sql
CREATE DATABASE ecommerce_lab3;
```

The project expects these database settings (see
`ecommerce_project/settings.py`, under `DATABASES`):

```python
'NAME':     'ecommerce_lab3'
'USER':     'deepika'
'PASSWORD': 'gautam'
'HOST':     'localhost'
'PORT':     '3306'
```

👉 **Change the `USER` and `PASSWORD`** in `settings.py` to match your own MySQL
credentials, or create a MySQL user that matches the values above.

### 6. Apply database migrations

This creates all the tables your app needs:

```bash
python manage.py migrate
```

### 7. Create an admin (superuser) account

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username and password. This account can access the
Django admin at `/admin/` and the staff management area.

### 8. (Optional) Load demo products

To fill the store with sample watches and categories so you have something to
see right away:

```bash
python load_sample_data.py
```

### 9. Run the development server

```bash
python manage.py runserver
```

Now open your browser and visit:

👉 **http://127.0.0.1:8000/**

---

## 🔑 Useful URLs

| Page                  | URL                          |
|-----------------------|------------------------------|
| Home                  | `/`                          |
| Shop                  | `/shop/`                     |
| Cart                  | `/cart/`                     |
| Login                 | `/accounts/login/`           |
| Sign up               | `/accounts/signup/`          |
| My orders             | `/orders/my-orders/`         |
| Manage products (staff)| `/manage/products/`         |
| Manage categories (staff)| `/manage/categories/`     |
| Manage orders (staff) | `/orders/manage/`            |
| Django admin          | `/admin/`                    |

> The **staff management area** (`/manage/...`) is only available to users with
> the *staff* flag enabled. Superusers created with `createsuperuser` have it by
> default.

---

## 📧 Password Reset Emails

For development, password-reset emails are printed to the **terminal** instead of
being sent for real. After requesting a reset, look in the terminal running the
server to find the reset link. This is controlled by this line in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## 🧪 Running the Tests

The project includes automated tests for accounts, products, the cart, and
checkout:

```bash
python manage.py test
```

Django creates a temporary **test database** when running tests. Your MySQL user
needs permission to create databases. If you see an *"Access denied ... to
database 'test_ecommerce_lab3'"* error, grant the permission once (as the MySQL
root user):

```sql
GRANT ALL PRIVILEGES ON test_ecommerce_lab3.* TO 'deepika'@'localhost';
FLUSH PRIVILEGES;
```

---

## 🛠️ Common Problems

| Problem | Solution |
|---------|----------|
| `No module named 'pymysql'` | Run `pip install -r requirements.txt` again. |
| `cryptography package is required` | Run `pip install cryptography`. |
| `Can't connect to MySQL server` | Make sure MySQL is running and the credentials in `settings.py` are correct. |
| `Unknown database 'ecommerce_lab3'` | Create the database (see step 5). |
| Images not showing | Make sure you ran the server with `DEBUG = True` (the default). |

---

## 📜 License

This project was created for educational purposes as a bachelor's degree project.
Feel free to use it for learning.
