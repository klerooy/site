.PHONY: up down restart logs ps

up:
	docker compose up --build -d

down:
	docker compose down

restart:
	docker compose down && docker compose up --build -d

logs:
	docker compose logs -f

ps:
	docker compose ps
