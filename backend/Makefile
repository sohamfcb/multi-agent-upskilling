# Detect OS
UNAME_S := $(shell uname -s)

ifeq ($(OS),Windows_NT)
    ACTIVATE = .\venv\Scripts\activate
    CAT = type
else
    ACTIVATE = . venv/bin/activate
    CAT = cat
endif

# Docker Compose command
DOCKER_COMPOSE := $(shell if command -v docker-compose >/dev/null 2>&1; then echo docker-compose; else echo "docker compose"; fi)

# Load env file
ENV_FILE := .env
ifneq (,$(wildcard $(ENV_FILE)))
  include $(ENV_FILE)
  export
endif

DB_CONTAINER ?= $(DB_CONTAINER)
DB_USER ?= $(DB_USER)
DB_NAME ?= $(DB_NAME)
DB_PORT ?= $(DB_PORT)

.PHONY: install db-up db-down wait-for-db db-migrate db-dump db-restore db-bootstrap init run

# --- Python environment ---
install:  ## Create venv and install dependencies
	python -m venv venv
	$(ACTIVATE) && pip install -r requirements.txt

# --- Alembic helpers ---
alembic-revision:  ## Create a new Alembic migration. Usage: make alembic-revision MSG="your message"
ifndef MSG
	$(error MSG is undefined. Example: make alembic-revision MSG="added new column to users")
endif
	python -m alembic revision --autogenerate -m "$(MSG)"
# --- Docker ---
db-up:  ## Start DB container
	$(DOCKER_COMPOSE) --env-file $(ENV_FILE) up -d

db-down:  ## Stop DB container
	$(DOCKER_COMPOSE) --env-file $(ENV_FILE) down

wait-for-db:  ## Wait until Postgres is ready
	@echo "⏳ Waiting for Postgres to be ready..."
	@until docker exec -i $(DB_CONTAINER) pg_isready -U $(DB_USER) > /dev/null 2>&1; do \
		sleep 1; \
	done
	@echo "✅ Postgres is ready!"

# --- Database ---
db-migrate:  ## Apply Alembic migrations
	python -m alembic upgrade head

# db-dump:  ## Dump schema + data to dump.sql
# 	docker exec -t $(DB_CONTAINER) pg_dump -U $(DB_USER) -d $(DB_NAME) > dump.sql

db-dump:  ## Dump schema + data to dump.sql
	docker exec $(DB_CONTAINER) pg_dump -U $(DB_USER) -d $(DB_NAME) -f /tmp/dump.sql
	docker cp $(DB_CONTAINER):/tmp/dump.sql ./dump.sql
	docker exec $(DB_CONTAINER) rm /tmp/dump.sql


db-restore:  ## Restore from dump.sql
	$(CAT) dump.sql | docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

db-bootstrap:  ## Full DB reset + migrations
	$(DOCKER_COMPOSE) --env-file $(ENV_FILE) down -v
	$(DOCKER_COMPOSE) --env-file $(ENV_FILE) up -d
	$(MAKE) wait-for-db
	$(MAKE) db-migrate

# --- Full setup ---
init: db-up wait-for-db db-migrate db-dump  ## Start DB, migrate, and dump
	@echo "✅ Database initialized and dump.sql updated!"

# --- Run backend ---
run:  ## Run backend server
	uvicorn app:app --reload --host 0.0.0.0 --port 8000
