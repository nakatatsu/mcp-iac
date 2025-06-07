.PHONY: install build deploy local clean test

# Install dependencies
install:
	pip install -r requirements.txt

# Build the SAM application
build:
	sam build

# Deploy to AWS (first time)
deploy-guided:
	sam deploy --guided

# Deploy to AWS (subsequent times)
deploy:
	sam deploy

# Run locally
local:
	sam local start-api --port 3000

# Run the application directly
run:
	cd src && python -m app

# Clean build artifacts
clean:
	rm -rf .aws-sam/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Validate SAM template
validate:
	sam validate

# Show logs
logs:
	sam logs --tail

# Test the deployed API
test-api:
	@echo "Testing list_documents endpoint..."
	@curl -X POST $${API_URL}mcp/tools/list_documents \
		-H "Content-Type: application/json" \
		-d '{}'

# Package for deployment
package:
	sam package --output-template-file packaged.yaml --s3-bucket $${S3_BUCKET}

commit:
	@git add . && git commit -m "Update" 

push:
	@git push
