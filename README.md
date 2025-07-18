# Todo App

A simple Django-based todo list application.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/HunterKnott/todo-app.git
   cd todo-app
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the app**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
   - Admin interface: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Note

- For development, emails are printed to the console.
