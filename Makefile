.PHONY: local
local:
	docker compose -f docker-compose.local.yml up

.PHONY: up-old
up-old:
	poetry run uvicorn main3:app --port 8000

.PHONY: up
up:
	poetry run uvicorn app:app --port 8000 --reload