build:
	docker build -t aiven/aiven .

initdb:
	scripts/create_table.sh

lint:
	@echo "Starting to lint checking..."
	flake8
	@echo "All done"

test:
	scripts/run_test.sh

monitor:
	@echo "Starting up monitor process..."
	docker-compose up monitor

etl:
	@echo "Starting up etl process..."
	docker-compose up etl

all:
	docker-compose up -d monitor etl
