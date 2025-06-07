from mcp.server.fastmcp import FastMCP
from mangum import Mangum
import os
import boto3
import yaml
from botocore.exceptions import ClientError
from typing import Dict, Any

# FastMCP サーバーを初期化
mcp = FastMCP(
    "mcp-iac-doc",
    stateless_http=True,
    json_response=True,
)

# 必須の環境変数
S3_BUCKET = os.environ["S3_BUCKET_NAME"]

# boto3 S3 クライアント（同期版）
s3 = boto3.client("s3")


@mcp.tool()
def test() -> dict:
    return {"status": "ok"}


@mcp.tool()
def get_document(document_name: str) -> Dict[str, Any]:
    possible_keys = [
        f"guidelines/{document_name}.yaml",
        f"processes/{document_name}.yaml",
        f"tasks/{document_name}.yaml",
        f"resouce_specifications/{document_name}.yaml",
        f"{document_name}.yaml"
    ]
    
    for key in possible_keys:
        try:
            response = s3.get_object(Bucket=S3_BUCKET, Key=key)
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
        "error": f"Document '{document_name}' not found in S3 bucket '{S3_BUCKET}'",
        "message": "Please check the document name and try again"
    }


app = mcp.streamable_http_app()

handler = Mangum(
    app,
    lifespan="on",
    api_gateway_base_path=os.getenv("API_GATEWAY_ROOT_PATH", ""),
)
