.PHONY: install run local clean test update

# Install dependencies
install:
	source venv/bin/activate && pip install -r requirements.txt

# Run the application directly
run:
	source venv/bin/activate && cd src && python lambda_function.py

# Run the application with script (optional port parameter)
local:
	source venv/bin/activate && ./scripts/local.sh

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
	@if [ -z "$$API_URL" ]; then \
		echo "API_URL not set, using local endpoint..."; \
		API_URL="http://localhost:8000/"; \
	else \
		echo "Using API_URL: $$API_URL"; \
	fi; \
	echo "Testing get_document endpoint..."; \
	curl -s -X POST $${API_URL}mcp/ \
		-H "Content-Type: application/json" \
		-H "Accept: application/json, text/event-stream" \
		-d '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "get_document", "arguments": {"document_name": "development_guidelines"}}, "id": 1}' | python -m json.tool

# Test API locally (convenience target)
test-local:
	@API_URL=http://localhost:8000/ make test-api

commit:
	@git add . && git commit -m "Update" 

push:
	@git push
