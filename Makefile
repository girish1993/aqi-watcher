.PHONY: run down airflow-init airflow-run

run:
	docker compose up

down:
	docker compose down

airflow-init:
	docker compose -f docker-compose.airflow.yaml up airflow-init