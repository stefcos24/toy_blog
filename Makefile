build:
	docker-compose --env-file .docker.env up --build -d

up:
	docker-compose --env-file .docker.env up -d

ssh:
	docker exec -it toyblog /bin/bash

server:
	docker exec -it toyblog python manage.py runserver 0.0.0.0:8000

down:
	docker-compose down

flake8:
	docker exec -it toyblog flake8 /toy_blog

test:
	docker exec -it toyblog python -m unittest discover
