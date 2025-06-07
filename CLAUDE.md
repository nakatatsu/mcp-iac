# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides Infrastructure as Code documentation to AI agents. It serves YAML-based documentation through MCP tools and can be deployed using Terraform.

## Common Commands

### Development
- `make install` - Install Python dependencies
- `make run` - Run the application directly (Python)
- `make local` - Run with local development script (port 8000)
- `./scripts/local.sh [port]` - Run with custom port
- `python -m app` (from src/) - Direct Python execution

### Deployment and Updates
- `ENVIRONMENT=development make update` - Update Lambda function code
- `./scripts/update.sh <environment>` - Direct script execution for updates

### Testing and Maintenance
- `make test-api` - Test deployed API endpoints (requires API_URL env var)
- `make clean` - Remove build artifacts and Python cache files

## Architecture

**Core Components:**
- **FastMCP Server** (`src/app/main.py`): Main application using FastMCP framework with 8 MCP tools
- **Documentation Store**: YAML files in `documents/` and `resouces_specification/` directories

**Key Tools Provided:**
- `list_documents` - List available documentation
- `get_document` - Retrieve specific documents by name  
- `get_development_guidelines` - Get development guidelines
- `get_module_*` - Various module templates and requirements
- `get_resource_specification` - AWS resource-specific rules
- `search_guidelines` - Keyword search across all documents

## Configuration

The project expects documentation files in:
- `documents/` - General documentation YAML files
- `resouces_specification/` - AWS resource-specific YAML files

Use Terraform for infrastructure deployment.

## Development Notes

The application uses stateless HTTP mode for compatibility with serverless deployments. Document paths are resolved relative to the application root.

## IMPORTANT: Lambda Handler Requirements

**DO NOT use Mangum** for Lambda integration. This project uses FastMCP's native `stateless_http=True` mode which provides direct Lambda compatibility without additional adapters.