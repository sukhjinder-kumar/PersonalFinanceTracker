# Project variables
IMAGE_NAME = personal_finance_tracker
DB_NAME = finance_tracker.db

.PHONY: all build populate analyze clean run

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run populate.py to add sample data
populate:
	docker run --rm -v $(PWD):/app $(IMAGE_NAME) python populate.py

# Run analysis.py to generate insights/plots
analyze:
	docker run --rm -v $(PWD):/app $(IMAGE_NAME) python analysis.py

# Chain build -> populate -> analyze
run: build populate analyze

# Remove the database file and any generated images
clean:
	rm -f $(DB_NAME)
	rm -f Images/monthly_spending_by_category.png
