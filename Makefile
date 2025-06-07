.PHONY: install run local clean test update

# Install dependencies
install:
	pip install -r requirements.txt

# Run the application directly
run:
	cd src && python -m app

# Run the application with script (optional port parameter)
local:
	./scripts/local.sh

# Clean build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Update Lambda function (requires ENVIRONMENT variable)
update:
	@if [ -z "$$ENVIRONMENT" ]; then \
		echo "Error: ENVIRONMENT variable is required"; \
		echo "Usage: ENVIRONMENT=development make update"; \
		exit 1; \
	fi
	./scripts/update.sh $$ENVIRONMENT

# Test the API (requires API_URL environment variable)
test-api:
	@echo "Testing list_documents endpoint..."
	@curl -X POST $${API_URL}mcp/tools/list_documents \
		-H "Content-Type: application/json" \
		-d '{}'

commit:
	@git add . && git commit -m "Update" 

push:
	@git push
