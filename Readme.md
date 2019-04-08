# stacks used
django, djangorestframework

# project setup
1. git clone https://github.com/Chandrabhushan01/myskinny.git
2. go to myskinny directory by: cd myskinny
3. create a virtualenv using: python3 -m venv . (install python3 on your machine if not already installed)
4. activate environment using: source bin/activate
5. upgrade pip using: pip install --upgrade pip
6. curl https://bootstrap.pypa.io/get-pip.py | python
7. install requirements using: pip install -r requirements.txt
8. create database schema using: python manage.py migrate
9. create a superuser: python manage.py createsuperuser
10. run: python manage.py runserver



# testbench
# request box list
API: api/v1/box/
Method:GET
FILTERS_KEY: 'length', 'min_length', 'max_length',
        'breadth', 'min_breadth', 'max_breadth',
        'height', 'min_height', 'max_height',
        'area', 'min_area', 'max_area',
        'volume', 'min_volume', 'max_volume',
        'created_at', 'created_before', 'created_after',
        'created_by', 'username' 

# create box
API: api/v1/box/
Method:POST
data: {"length": 5, "breadth": 5, "height": 5}
(only staff user can create box)

# update box
API: api/v1/box/box_id/
Method:PATCH
data: {"length": 5, "breadth": 7, "height": 10}
(only staff user can update box)
