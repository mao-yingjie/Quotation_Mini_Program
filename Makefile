.PHONY: install init-db

# Install dependencies including runtime and development extras
install:
	poetry install -E runtime -E dev

# Initialize the application's database
init-db:
	poetry run contractor init-db
