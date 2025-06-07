#!/bin/bash

# Local development script
# Usage: ./scripts/local.sh [port]
# Example: ./scripts/local.sh 8080

set -e

# Default port
PORT=${1:-8000}

echo "Starting MCP IaC Documentation Server locally on port ${PORT}..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please create one with: python3 -m venv venv"
    exit 1
fi

# Set environment variables for local development
export PYTHONPATH="src"
export PORT="${PORT}"
export S3_BUCKET_NAME="${S3_BUCKET_NAME:-development-tfdoc}"

# Change to src directory and run the application
cd src
python lambda_function.py