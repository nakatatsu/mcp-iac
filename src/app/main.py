import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from fastmcp import FastMCP

# Create MCP instance with stateless HTTP mode for Lambda
mcp = FastMCP(
    stateless_http=True,
    json_response=True,
    name="mcp-iac-doc",
    version="1.0.0"
)

# Base path for documents
BASE_PATH = Path(__file__).parent.parent.parent.parent
DOCUMENTS_PATH = BASE_PATH / "documents"
RESOURCES_PATH = BASE_PATH / "resouces_specification"


@mcp.tool()
def list_documents() -> Dict[str, List[str]]:
    """List all available documentation files"""
    result = {
        "documents": [],
        "resource_specifications": []
    }
    
    # List documents
    if DOCUMENTS_PATH.exists():
        for file in DOCUMENTS_PATH.glob("*.yaml"):
            result["documents"].append(file.stem)
    
    # List resource specifications
    if RESOURCES_PATH.exists():
        for file in RESOURCES_PATH.glob("*.yaml"):
            result["resource_specifications"].append(file.stem)
    
    return result


@mcp.tool()
def get_document(document_name: str) -> Dict[str, any]:
    """Get a specific document by name"""
    # Try documents directory first
    doc_path = DOCUMENTS_PATH / f"{document_name}.yaml"
    if doc_path.exists():
        with open(doc_path, 'r', encoding='utf-8') as f:
            return {
                "type": "document",
                "name": document_name,
                "content": yaml.safe_load(f)
            }
    
    # Try resource specifications
    resource_path = RESOURCES_PATH / f"{document_name}.yaml"
    if resource_path.exists():
        with open(resource_path, 'r', encoding='utf-8') as f:
            return {
                "type": "resource_specification",
                "name": document_name,
                "content": yaml.safe_load(f)
            }
    
    return {
        "error": f"Document '{document_name}' not found",
        "available": list_documents()
    }


@mcp.tool()
def get_development_guidelines() -> Dict[str, any]:
    """Get the development guidelines document"""
    return get_document("development_guidelines")


@mcp.tool()
def get_module_code_template() -> Dict[str, any]:
    """Get the module code generation template"""
    return get_document("module_code")


@mcp.tool()
def get_module_requirements() -> Dict[str, any]:
    """Get the module requirements specification"""
    return get_document("module_requirements")


@mcp.tool()
def get_module_specification_template() -> Dict[str, any]:
    """Get the module specification template"""
    return get_document("module_specification")


@mcp.tool()
def get_task_process() -> Dict[str, any]:
    """Get the standard task process workflow"""
    return get_document("task_process")


@mcp.tool()
def get_resource_specification(resource_type: str) -> Dict[str, any]:
    """Get resource-specific rules and specifications
    
    Args:
        resource_type: The AWS resource type (e.g., 's3', 'cloudwatch_logs')
    """
    return get_document(resource_type)


@mcp.tool()
def search_guidelines(keyword: str) -> Dict[str, List[Dict[str, any]]]:
    """Search for specific guidelines or rules containing the keyword
    
    Args:
        keyword: The keyword to search for in all documents
    """
    results = []
    
    # Search in all documents
    all_paths = []
    if DOCUMENTS_PATH.exists():
        all_paths.extend(DOCUMENTS_PATH.glob("*.yaml"))
    if RESOURCES_PATH.exists():
        all_paths.extend(RESOURCES_PATH.glob("*.yaml"))
    
    for file_path in all_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if keyword.lower() in content.lower():
                # Load YAML and find matching sections
                data = yaml.safe_load(content)
                matches = _search_in_dict(data, keyword, file_path.stem)
                results.extend(matches)
    
    return {"results": results, "total": len(results)}


def _search_in_dict(data: any, keyword: str, source: str, path: str = "") -> List[Dict[str, any]]:
    """Recursively search for keyword in dictionary/list structures"""
    matches = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            if keyword.lower() in str(key).lower():
                matches.append({
                    "source": source,
                    "path": new_path,
                    "key": key,
                    "value": value
                })
            matches.extend(_search_in_dict(value, keyword, source, new_path))
    
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            if isinstance(item, str) and keyword.lower() in item.lower():
                matches.append({
                    "source": source,
                    "path": new_path,
                    "value": item
                })
            else:
                matches.extend(_search_in_dict(item, keyword, source, new_path))
    
    elif isinstance(data, str):
        if keyword.lower() in data.lower():
            matches.append({
                "source": source,
                "path": path,
                "value": data
            })
    
    return matches


# Create the app instance for Lambda
app = mcp.get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)