# 🕒 Watch House — Django E-Commerce Store

Watch House is an online store for selling watches, built with **Django** and
**MySQL**. It has a modern, responsive **dark theme** and covers everything a
small online shop needs: browsing products, search and filters, a shopping
cart, checkout, order history, user accounts, and a staff area for managing
products and orders.

This is a **college project** made for learning how a real Django web
application is built and organised.

---

## ✨ Features

- 🏠 **Home page** with featured products and categories
- 🛍️ **Shop page** with category filtering, keyword search, and pagination
- 🔎 **Product detail** pages with related products
- 🛒 **Shopping cart** — add, update quantity, and remove items
- 💳 **Checkout** with shipping details and payment options
- 📦 **Order history** — customers can see their past orders
- 👤 **User accounts** — sign up, log in, log out, and password reset
- 🔧 **Staff area** — create, edit, and delete products & categories
- 📋 **Order management** — staff update order status
  (Pending → Processing → Shipped → Delivered / Cancelled)
- 🎨 **Responsive dark UI** built on Bootstrap 5
- ⚙️ **Django admin** for full back-office control

---

## 🧰 Tech Stack

| Layer    | Technology                         |
|----------|------------------------------------|
| Backend  | Python, Django 5+                  |
| Database | MySQL                              |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Icons    | Font Awesome                       |

---

## 📁 Project Structure

```
ecommerce-project/          <-- repository root (run all commands here)
│   manage.py
│   requirements.txt
│   load_sample_data.py     <-- script to add demo products
│   .env                    <-- your secret settings (NOT on GitHub)
│   .env.example            <-- template for the .env file
│   README.md
│
├── ecommerce_project/      <-- project settings & URLs
├── accounts/               <-- users, login, signup, password reset
├── products/               <-- products, categories, cart
├── orders/                 <-- checkout and orders
├── templates/              <-- all HTML pages
├── static/                 <-- CSS, JavaScript, images
└── media/                  <-- uploaded product/category images
```

> ⚠️ Run every `python manage.py ...` command from the **repository root**
> (the folder that contains `manage.py`).

---

## 🚀 How to Run This Project

Follow these steps in order.

### 1. Install the required software

- [Python 3.10+](https://www.python.org/downloads/)
- [MySQL Server 8+](https://dev.mysql.com/downloads/mysql/)
- [Git](https://git-scm.com/downloads)

### 2. Get the code

```bash
git clone <your-repository-url>
cd ecommerce-project
```

### 3. Create and activate a virtual environment

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

### 6. Create your `.env` file (secret settings)

Passwords and the secret key are **not** written in the code. They go in a file
called `.env`. Git ignores this file, so your passwords never go to GitHub.

Make your own copy from the example file:

**Windows**
```bash
copy .env.example .env
```

**macOS / Linux**
```bash
cp .env.example .env
```

Now open `.env` in a text editor and fill in your values:

```
SECRET_KEY=any-long-random-string-of-your-choice
DEBUG=True

DB_NAME=ecommerce_lab3
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

- **`DB_USER` / `DB_PASSWORD`** — use your own MySQL username and password.
- **`SECRET_KEY`** — any long random string. To generate a good one, run:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

> 🔒 Never share or commit the `.env` file. Only `.env.example` (with fake
> placeholder values) belongs on GitHub.

### 7. Create the database tables

```bash
python manage.py migrate
```

### 8. Create an admin (superuser) account

```bash
python manage.py createsuperuser
```

Follow the prompts. This account can log in to the Django admin at `/admin/`
and the staff area.

### 9. (Optional) Load demo products

To fill the store with sample watches so you have something to see:

```bash
python load_sample_data.py
```

### 10. Start the server

```bash
python manage.py runserver
```

Then open your browser and visit 👉 **http://127.0.0.1:8000/**

---

## 🔑 Useful URLs

| Page                      | URL                    |
|---------------------------|------------------------|
| Home                      | `/`                    |
| Shop                      | `/shop/`               |
| Cart                      | `/cart/`               |
| Login                     | `/accounts/login/`     |
| Sign up                   | `/accounts/signup/`    |
| My orders                 | `/orders/my-orders/`   |
| Manage products (staff)   | `/manage/products/`    |
| Manage categories (staff) | `/manage/categories/`  |
| Manage orders (staff)     | `/orders/manage/`      |
| Django admin              | `/admin/`              |

> The **staff area** (`/manage/...`) only works for users with the *staff* flag.
> Superusers made with `createsuperuser` have it by default.

---

## 📧 Password Reset Emails

In development, password-reset emails are printed to the **terminal** instead of
being sent for real. After requesting a reset, look in the terminal running the
server to find the reset link.

---

## 🧪 Running the Tests

The project has tests for accounts, products, the cart, and checkout:

```bash
python manage.py test
```

Django makes a temporary **test database** when running tests, so your MySQL
user needs permission to create databases. If you see an *"Access denied ... to
database 'test_ecommerce_lab3'"* error, grant it once as the MySQL root user
(replace `your_mysql_username` with the `DB_USER` from your `.env`):

```sql
GRANT ALL PRIVILEGES ON test_ecommerce_lab3.* TO 'your_mysql_username'@'localhost';
FLUSH PRIVILEGES;
```

---

## 🛠️ Common Problems

| Problem | Solution |
|---------|----------|
| `No module named 'pymysql'` / `No module named 'dotenv'` | Run `pip install -r requirements.txt` again. |
| `cryptography package is required` | Run `pip install cryptography`. |
| `Can't connect to MySQL server` | Make sure MySQL is running and the credentials in your `.env` are correct. |
| `SECRET_KEY ... must not be empty` | Make sure you created the `.env` file (step 6) and set a `SECRET_KEY`. |
| `Unknown database 'ecommerce_lab3'` | Create the database (see step 5). |
| `.env` values not loading | The file must be named exactly `.env` and sit in the repository root next to `manage.py`. |
| Images not showing | Make sure `DEBUG=True` is set in your `.env`. |

---

## 📜 License

This project was created for educational purposes as a college project.
Feel free to use it for learning.
