.PHONY: build up down logs logs-items logs-reviews logs-frontend logs-mysql clean test shell-mysql help

help:
	@echo "ICU v1.0.0 - Available Commands"
	@echo "================================"
	@echo "make build        - Build all Docker images"
	@echo "make up           - Start all services with docker-compose"
	@echo "make down         - Stop all services"
	@echo "make logs         - View logs from all services"
	@echo "make logs-items   - View only Items service logs"
	@echo "make logs-reviews - View only Reviews service logs"
	@echo "make logs-frontend - View only Frontend service logs"
	@echo "make logs-mysql   - View only MySQL logs"
	@echo "make test         - Run all service tests"
	@echo "make shell-mysql  - Open MySQL shell"
	@echo "make clean        - Remove containers and images"
	@echo "make help         - Show this help message"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

logs-items:
	docker compose logs -f items-service

logs-reviews:
	docker compose logs -f reviews-service

logs-frontend:
	docker compose logs -f frontend

logs-mysql:
	docker compose logs -f mysql

shell-mysql:
	docker compose exec mysql mysql -u root -proot icu_v1

test:
	docker compose exec -T items-service python -m pytest test_items.py -v
	docker compose exec -T reviews-service mvn test

clean:
	docker compose down
	docker rmi demo-web-app-items-service demo-web-app-reviews-service demo-web-app-frontend 2>/dev/null || true
