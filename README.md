# Calendar app
Web calendar in django for crud control of events


# Usage
Clone this repo, setup virtualenv, install Django
```
git clone https://github.com/lucasribeirorsousa/calendar-app.git
cd calendar-app

python -m venv venv
venv\Scripts\activate
source venv/bin/activate

pip install -r requirements.txt

python manage.py createsuperuser

python manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
Find the app running at http://localhost:8000/calendar/