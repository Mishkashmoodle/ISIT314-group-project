uMatch — Setup and Run Guide

PREREQUISITES
- Python 3.12 or newer
- Internet connection

SETUP INSTRUCTIONS

1. Open a terminal in the project root folder.

2. Create a virtual environment

   macOS / Linux:
       python3 -m venv .venv

   Windows:
       python -m venv .venv

3. Activate the virtual environment

   macOS / Linux:
       source .venv/bin/activate

   Windows:
       .venv\Scripts\activate

4. Install required dependencies

   macOS / Linux:
       pip install django djangorestframework django-cors-headers pdfplumber python-docx

   Windows:
       pip install django djangorestframework django-cors-headers pdfplumber python-docx

   Note: Once the virtual environment is active, pip points to the right place
   on both platforms. (On macOS you can also use pip3 if pip isn't found.)

5. Navigate to the Django project folder

   Stay in the root directory.

6. Apply database migrations

   macOS / Linux:
       python3 manage.py migrate

   Windows:
       python manage.py migrate

7. Start the Django server

   macOS / Linux:
       python3 manage.py runserver

   Windows:
       python manage.py runserver

The backend API should now be available at:

   http://127.0.0.1:8000/

Examples:
   http://127.0.0.1:8000/api/candidates/
   http://127.0.0.1:8000/api/jobs/
   http://127.0.0.1:8000/api/businesses/

FRONTEND

1. Open the frontend files in a browser.
2. Open: Main.html
3. Ensure the Django server is running before using the website.

Demo accounts are included in "Fake Accounts.txt", however any number of
accounts can be created from scratch.

NOTES
- Uploaded resumes are stored locally in the media/resumes folder.
- The database uses SQLite and is included with the project.
- If job listings, candidates, or businesses do not appear, ensure migrations
  have been applied and the Django server is running.
- If dependencies are missing, install them using pip before starting the server.

TROUBLESHOOTING
- "python" not found (macOS): macOS doesn't always alias python to Python 3.
  Use python3 instead.
- "pip" not found (macOS): Use pip3, or make sure your virtual environment is
  activated.
- Activation fails on Windows PowerShell: If .venv\Scripts\activate is blocked,
  run "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass" first, or use
  .venv\Scripts\activate.bat in Command Prompt.
- Port already in use: Run the server on a different port, e.g.
  python3 manage.py runserver 8001.
