# To create apps in Django

python manage.py startapp accounts
python manage.py startapp students
python manage.py startapp lecturers
python manage.py startapp subjects
python manage.py startapp classes
python manage.py startapp attendance
python manage.py startapp leaves
python manage.py startapp notifications
python manage.py startapp audit
python manage.py startapp rooms

# To migrate all app
python manage.py makemigrations accounts
python manage.py makemigrations subjects
python manage.py makemigrations students
python manage.py makemigrations lecturers
python manage.py makemigrations classes
python manage.py makemigrations rooms
python manage.py makemigrations attendance
python manage.py makemigrations audit
python manage.py makemigrations leaves
python manage.py makemigrations notifications

Then 

python manage.py migrate accounts
python manage.py migrate subjects
python manage.py migrate students
python manage.py migrate lecturers
python manage.py migrate classes
python manage.py migrate rooms
python manage.py migrate attendance
python manage.py migrate audit
python manage.py migrate leaves
python manage.py migrate notifications

# To seed data like laravel, you can create folders: [your_name_apps]/management/commands/[your_name_file]
# Then you can run the command in the terminal like this: python manage.py [your_name_file]
# Beside, you must create files in management/__init__.py and commands/__init__.py
python manage.py seed_role
python manage.py seed_academic_year
python manage.py seed_department 
python manage.py seed_major 
python manage.py seed_semester