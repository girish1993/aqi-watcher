.PHONY: timescale-run timescale-down airflow-init airflow-run airflow-down code-format

timescale-run:
	docker compose -f docker-compose.timescale.yaml build && docker compose -f docker-compose.timescale.yaml up

timescale-down:
	docker compose -f docker-compose.timescale.yml down

airflow-init:
	docker compose -f docker-compose.airflow.yaml up airflow-init

airflow-run:
	docker compose -f docker-compose.airflow.yaml build && docker compose -f docker-compose.airflow.yaml up

airflow-down:
	docker compose -f docker-compose.airflow.yaml down

code-format:
	black app/

