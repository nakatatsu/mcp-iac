import os
import yaml
import boto3
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP
from botocore.exceptions import ClientError

# Create MCP instance with stateless HTTP mode for Lambda
mcp = FastMCP(
    stateless_http=True,
    json_response=True,
    name="mcp-iac-doc",
    version="1.0.0"
)

# S3 bucket configuration
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'development-tfdoc')
if not S3_BUCKET_NAME:
    raise ValueError("S3_BUCKET_NAME environment variable is required")

# Initialize S3 client
s3_client = boto3.client('s3')


@mcp.tool()
def test() -> Dict[str, str]:
    """Simple test endpoint"""
    return {"status": "ok", "message": "Server is working"}

@mcp.tool()
def get_document(document_name: str) -> Dict[str, Any]:
    """Get a specific document by name from S3
    
    Args:
        document_name: The name of the document to retrieve (without .yaml extension)
    
    Returns:
        Dictionary containing the document content or error message
    """
    # Check all possible S3 keys based on S3 structure
    possible_keys = [
        f"guidelines/{document_name}.yaml",
        f"processes/{document_name}.yaml",
        f"tasks/{document_name}.yaml",
        f"resouce_specifications/{document_name}.yaml",
        f"{document_name}.yaml"
    ]
    
    for key in possible_keys:
        try:
            response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key)
            content = response['Body'].read().decode('utf-8')
            return yaml.safe_load(content)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                continue
            else:
                return {
                    "error": f"Error accessing S3: {str(e)}",
                    "message": "Please check S3 permissions and bucket configuration"
                }
    
    return {
        "error": f"Document '{document_name}' not found in S3 bucket '{S3_BUCKET_NAME}'",
        "message": "Please check the document name and try again"
    }


# Create the app instance for Lambda
app = mcp.http_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)