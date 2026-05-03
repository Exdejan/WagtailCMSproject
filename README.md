# My Wagtail Site

This is a Wagtail project built with Django.

## What This README Covers

- Windows setup and local run steps
- Basic Wagtail admin access
- Collaboration workflow for team members

## Run on Windows

### 1. Install Python

- Install Python 3.12 or newer from https://www.python.org/downloads/
- During installation, make sure **Add Python to PATH** is checked.

### 2. Open the project folder

Open a terminal in the project folder:

```powershell
cd C:\path\to\my-wagtail-site
```

### 3. Create a virtual environment

```powershell
py -m venv venv
```

### 4. Activate the virtual environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once first:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Command Prompt:

```bat
venv\Scripts\activate.bat
```

### 5. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Run migrations

```powershell
python manage.py migrate
```

### 7. Start the development server

```powershell
python manage.py runserver
```

Open the site in your browser:

```text
http://127.0.0.1:8000/
```

## Admin panel

If you want to log in to Wagtail admin, open:

```text
http://127.0.0.1:8000/admin/
```

If you do not have a superuser yet, create one with:

```powershell
python manage.py createsuperuser
```

## Collaboration Workflow

If another person is working on this project, use this flow:

### 1. Clone the repository

```powershell
git clone <repo-url>
cd my-wagtail-site
```

### 2. Get the latest changes

Before starting work:

```powershell
git pull origin main
```

### 3. Create a branch

```powershell
git checkout -b feature/my-change
```

### 4. Make your changes

- Edit templates, styles, or models as needed.
- If you change a model, create a migration.
- If you change static files, reload the page after a hard refresh.

### 5. Run the project locally

```powershell
python manage.py migrate
python manage.py runserver
```

### 6. Check what changed

```powershell
git status
```

### 7. Commit and push

```powershell
git add .
git commit -m "Describe your change"
git push origin feature/my-change
```

## Notes

- The homepage content is managed through Wagtail.
- Static files are loaded automatically during development.
- If you change the page layout or models, run `python manage.py makemigrations` and `python manage.py migrate` again.
- If the browser does not show your CSS changes, do a hard refresh with Ctrl+Shift+R.