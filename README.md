# Python CMS Manual

-This guide explains how to set up and run the Python CMS from scratch, including installing Python, setting up the environment, and running the CMS locally.

## 1. Install Python

- Go to the official Python website: https://www.python.org/downloads/

- Download the latest stable version of Python (recommended 3.11 or higher).

- Run the installer:

On Windows: Make sure to check Add Python to PATH before clicking Install.

On Mac or Linux: Follow the installer instructions or use a package manager (e.g., brew install python on Mac).

- Verify installation:
Open a terminal or command prompt and type:
```bash
python --version
```

It should display the Python version installed.

## 2. Install Git

- Go to https://git-scm.com/downloads

- Download and install Git for your system.

- Verify installation:
```bash
git --version
```

## 3. Clone the CMS repository

- Open a terminal or command prompt.

- Navigate to the folder where you want to store the project:
```bash
cd path/to/your/projects
```

-Clone the repository:
```bash
git clone https://github.com/yourusername/pythoncms.git
```

- Enter the project folder:
```bash
cd pythoncms
```
## 4. Create a virtual environment

A virtual environment ensures the project’s dependencies are separate from your system Python.

- Create the virtual environment:
```bash
python -m venv venv
```

- Activate the virtual environment:

#### Windows:
```bash
venv\Scripts\activate
```

#### Mac/Linux:
```bash
source venv/bin/activate
```

You should see (venv) at the start of your terminal prompt.

## 5. Install dependencies

Make sure you are in the project folder and the virtual environment is active.

- Install required packages:
```bash
pip install -r requirements.txt
```
## 6. Set up the database

This CMS uses SQLite by default (no extra installation needed).

- Apply migrations:
```bash
python manage.py migrate
```

- Create a superuser to access the admin panel:
```bash
python manage.py createsuperuser
```

- Enter a username, email, and password when prompted.

## 7. Run the development server
- Start the Django development server:
```bash
python manage.py runserver
```

### Open a browser and go to:

http://127.0.0.1:8000/
