# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides Infrastructure as Code documentation to AI agents. It's deployed as an AWS Lambda function and serves documentation from S3 storage using the FastMCP framework.

## Common Commands

### Development
- `make install` - Install Python dependencies
- `make run` - Run the application directly (requires `cd src && python main.py`)
- `make local` - Run with local development script on port 8000
- `./scripts/local.sh [port]` - Run with custom port (defaults to 8000)

### Deployment and Updates
- `ENVIRONMENT=development make update` - Update Lambda function code
- `./scripts/update.sh <environment>` - Direct script execution for updates

### Testing and Maintenance
- `make test-api` - Test deployed API endpoints (requires API_URL env var)
- `make test-local` - Test API on localhost:8000
- `make clean` - Remove build artifacts and Python cache files
- `make commit` - Add all changes and commit with "Update" message
- `make push` - Push to git repository

## Architecture

**Core Components:**
- **Lambda Function** (`src/lambda_function.py`): Main entry point using FastMCP with Mangum for AWS Lambda
- **S3 Storage**: Documentation stored in S3 bucket with organized folder structure
- **FastMCP Framework**: Provides MCP protocol implementation with HTTP stateless mode

**Current MCP Tools:**
- `test` - Simple health check endpoint
- `get_document` - Retrieve specific documents by name from S3

**S3 Structure:**
The application searches for documents in these S3 paths:
- `guidelines/{document_name}.yaml`
- `processes/{document_name}.yaml`
- `tasks/{document_name}.yaml`
- `resouce_specifications/{document_name}.yaml`
- `{document_name}.yaml`

## Configuration

**Required Environment Variables:**
- `S3_BUCKET_NAME` - S3 bucket containing documentation files

**Local Development:**
- `S3_BUCKET_NAME` defaults to `development-tfdoc` if not set
- `PYTHONPATH` is set to `src/` for module resolution

## Dependencies

Key Python packages (see `requirements.txt`):
- `fastmcp>=0.1.0` - MCP framework
- `boto3>=1.26.0` - AWS SDK
- `mangum>=0.17.0` - ASGI adapter for AWS Lambda
- `uvicorn>=0.30.0` - ASGI server for local development
- `pyyaml>=6.0` - YAML parsing

## Development Notes

- The application uses stateless HTTP mode for Lambda compatibility
- Lambda function name follows pattern: `{environment}-tfdoc`
- Deployment creates a zip package with dependencies and uploads to AWS Lambda
- Document retrieval searches multiple S3 paths automatically
- Error handling includes S3 access issues and missing documents

## File Structure

```
src/
├── lambda_function.py    # Main Lambda handler and MCP server
scripts/
├── local.sh             # Local development server
└── update.sh            # Lambda deployment script
```