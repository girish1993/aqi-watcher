.PHONY: run down airflow-init airflow-run airflow-down code-format

run:
	docker compose up

down:
	docker compose down

airflow-init:
	docker compose -f docker-compose.airflow.yaml up airflow-init

airflow-run:
	docker compose -f docker-compose.airflow.yaml build && docker compose -f docker-compose.airflow.yaml up

airflow-down:
	docker compose -f docker-compose.airflow.yaml down

code-format:
	black app/

