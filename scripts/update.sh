#!/bin/bash

# Lambda function update script using AWS CLI
# Usage: ./update.sh <environment>
# Example: ./update.sh development

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <environment>"
    echo "Example: $0 development"
    exit 1
fi

ENVIRONMENT=$1
FUNCTION_NAME="${ENVIRONMENT}-tfdoc"
TEMP_DIR=$(mktemp -d)

echo "Updating Lambda function: ${FUNCTION_NAME}"

# Create deployment package
echo "Creating deployment package..."

# Install dependencies to temp directory
echo "Installing dependencies..."
pip install -r requirements.txt -t "${TEMP_DIR}/package" --platform manylinux2014_x86_64 --implementation cp --python-version 3.13 --only-binary=:all:

# Copy application code
echo "Copying application code..."
cp -r src/* "${TEMP_DIR}/package/"

# Create zip file
cd "${TEMP_DIR}/package"
zip -r "${TEMP_DIR}/deployment.zip" . -x "__pycache__/*" "*.pyc" "*.dist-info/*"
cd -

# Update function code
echo "Updating function code..."
aws lambda update-function-code \
    --function-name "${FUNCTION_NAME}" \
    --zip-file "fileb://${TEMP_DIR}/deployment.zip"

# Wait for update to complete
echo "Waiting for update to complete..."
aws lambda wait function-updated \
    --function-name "${FUNCTION_NAME}"

# Clean up
rm -rf "${TEMP_DIR}"

echo "Update completed successfully!"
echo "Function: ${FUNCTION_NAME}"