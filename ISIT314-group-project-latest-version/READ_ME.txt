HOW TO RUN THE PROJECT

1. Open the project folder

2. Open a terminal in the root directory:
	ISIT314-group-project

3. Create a virtual environment
	Run:
		python -m venv venv

4. Activate the virtual environment

	a. If using PowerShell:
	First run:
		Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

	Then activate:
		venv\Scripts\Activate.ps1

	b. If using Command Prompt:
		venv\Scripts\activate

5. Install required libraries
	Run:
		pip install django djangorestframework

6. Create migrations
	Run:
		python manage.py makemigrations


7. Apply migrations
	Run:
		python manage.py migrate


8. Start the server
	Run:
		python manage.py runserver


9. Test the API
	Open in browser:
		http://127.0.0.1:8000/api/candidates/

		http://127.0.0.1:8000/api/jobs/

If working correctly, these should return:
[]