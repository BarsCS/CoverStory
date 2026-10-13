# 📚 CoverStory

**CoverStory** is a Django-based web application designed for book lovers to track their reading progress, organize personal bookshelves, search for canonical books, and share reviews and ratings.

---

## 🛠 Tech Stack

* **Language:** <img src="https://cdn.simpleicons.org/python/3776AB" alt="Python" width="20" height="20" style="vertical-align: middle;"/> **Python 3.x**
* **Backend Framework:** <img src="https://cdn.simpleicons.org/django/092E20" alt="Django" width="20" height="20" style="vertical-align: middle;"/> **Django** *(Views, Templates, ORM)*
* **Database:** <img src="https://cdn.simpleicons.org/postgresql/4169E1" alt="PostgreSQL" width="20" height="20" style="vertical-align: middle;"/> **PostgreSQL**
* **Caching:** <img src="https://cdn.simpleicons.org/redis/DC382D" alt="Redis" width="20" height="20" style="vertical-align: middle;"/> **Redis**
* **Version Control:** <img src="https://cdn.simpleicons.org/git/F05032" alt="Git" width="20" height="20" style="vertical-align: middle;"/> **Git** & <img src="https://cdn.simpleicons.org/github/181717" alt="GitHub" width="20" height="20" style="vertical-align: middle;"/> **GitHub**

---

## ✨ Key Features

* 👤 **User Management & Authentication:** User registration, login/logout system, and profile management.
* 📖 **Canonical Book Database:** Centralized catalog for searching and browsing books.
* 🔖 **Personal Bookshelves:** Categorize books into custom shelves (e.g., *Want to Read*, *Currently Reading*, *Read*).
* ⭐ **Reviews & Ratings:** Ability to leave detailed reviews and rate books.
* ⚡ **Performance Optimization:** Integrated **Redis** for basic response and view caching to reduce database load on frequent queries.

---

## 🚀 Local Setup & Installation

Follow these steps to run the project locally on your machine.

### 📋 Prerequisites

Ensure you have the following installed and running:
* <img src="https://cdn.simpleicons.org/python/3776AB" alt="Python" width="18" height="18" style="vertical-align: middle;"/> **Python 3.10+**
* <img src="https://cdn.simpleicons.org/postgresql/4169E1" alt="PostgreSQL" width="18" height="18" style="vertical-align: middle;"/> **PostgreSQL** *(running locally)*
* <img src="https://cdn.simpleicons.org/redis/DC382D" alt="Redis" width="18" height="18" style="vertical-align: middle;"/> **Redis** *(running locally on port 6379)*

---

### Step 1: Clone the Repository

git clone https://github.com/your-username/coverstory.git
cd coverstory

---

### Step 2: Create and Activate Virtual Environment

On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

On Windows:
python -m venv venv
venv\Scripts\activate

---

### Step 3: Install Dependencies

pip install -r requirements.txt

---

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory based on your setup:

SECRET_KEY=your_secret_key_here
DEBUG=True

# <img src="https://cdn.simpleicons.org/postgresql/4169E1" alt="PostgreSQL" width="16" height="16"/> Database Configuration
DB_NAME=coverstory_db

DB_USER=postgres

DB_PASSWORD=your_password

DB_HOST=localhost

DB_PORT=5432

# <img src="https://cdn.simpleicons.org/redis/DC382D" alt="Redis" width="16" height="16"/> Redis Configuration
REDIS_URL=redis://127.0.0.1:6379/1

---

### Step 5: Database Migrations & Superuser

Apply database migrations:
python manage.py migrate

(Optional) Create an admin account:
python manage.py createsuperuser

---

### Step 6: Run the Server

Make sure your **Redis** and **PostgreSQL** services are running locally, then start the Django development server:

python manage.py runserver

Open your browser and navigate to http://127.0.0.1:8000/.

---

## 📝 License

This project was developed for educational and portfolio purposes.