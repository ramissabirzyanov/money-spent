install:
		pip install -r requirements.txt

freeze:
		pip freeze > requirements.txt

run:
		python3 main.py

lint:
		python3 -m flake8
