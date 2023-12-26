run:
	docker compose up --build

test:
	docker compose exec app pytest
