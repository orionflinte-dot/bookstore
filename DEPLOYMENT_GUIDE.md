# Deployment Guide

Follow these steps to upload your project to **GitHub** and deploy it to **PythonAnywhere**.

---

## Part 1: Uploading to GitHub

### 1. Initialize Git locally
Open your terminal in the `bookstore` folder and run:
```powershell
git init
git add .
git commit -m "Initial commit: Modern Bookstore"
```

### 2. Create a GitHub Repository
1. Go to [github.com](https://github.com/) and log in.
2. Click **New** (green button) to create a new repository.
3. Name it `bookstore` (or your choice).
4. **DO NOT** check "Initialize this repository with a README" (we already have one).
5. Click **Create repository**.

### 3. Push your code
Copy the commands from the GitHub "Quick setup" page (specifically the ones under "...or push an existing repository from the command line"):
```powershell
git remote add origin https://github.com/YOUR_USERNAME/bookstore.git
git branch -M main
git push -u origin main
```

---

## Part 2: Deploying to PythonAnywhere

### 1. Create a PythonAnywhere account
Go to [pythonanywhere.com](https://www.pythonanywhere.com/) and sign up for a **Beginner (Free)** account.

### 2. Clone your repository
1. Go to the **Consoles** tab.
2. Open a **Bash** console.
3. Run the following command:
   ```bash
   git clone https://github.com/YOUR_USERNAME/bookstore.git
   cd bookstore
   ```

### 3. Create a Virtual Environment
In the same Bash console, run:
```bash
mkvirtualenv --python=/usr/bin/python3.10 bookstore-venv
pip install -r requirements.txt
```

### 4. Setup the Web App
1. Go to the **Web** tab on the PythonAnywhere dashboard.
2. Click **Add a new web app**.
3. Click **Next** -> Select **Manual configuration** (NOT "Django") -> Select **Python 3.10**.
4. Set the **Source code** path: `/home/YOUR_USERNAME/bookstore`
5. Set the **Working directory** path: `/home/YOUR_USERNAME/bookstore`
6. Under **Virtualenv**, enter the name: `bookstore-venv`

### 5. Configure WSGI File
1. Under the **Web** tab, find "Code" -> **WSGI configuration file**.
2. Click the link to edit it.
3. Replace the ENTIRE content with this:
```python
import os
import sys

path = '/home/YOUR_USERNAME/bookstore'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Replace `YOUR_USERNAME` with your actual PythonAnywhere username!)*

### 6. Static Files (Web Tab)
Scroll down to the **Static files** section and add these two:
- **URL:** `/static/`  ->  **Path:** `/home/YOUR_USERNAME/bookstore/staticfiles`
- **URL:** `/media/`   ->  **Path:** `/home/YOUR_USERNAME/bookstore/media`

### 7. Run Migrations & Collect Static
Go back to your Bash console in PythonAnywhere:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 8. Final Step: Reload
Go back to the **Web** tab and click the green **Reload** button at the top. Your site should now be live at `YOUR_USERNAME.pythonanywhere.com`!

---

## Part 3: Updating the site
Whenever you make changes locally:
1. `git add .` -> `git commit -m "Update"` -> `git push`
2. Go to PythonAnywhere Bash: `git pull`
3. Reload the Web App.
