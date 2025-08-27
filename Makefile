.PHONY: build up down index

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

index:
	docker compose run --rm web python manage.py index_books
