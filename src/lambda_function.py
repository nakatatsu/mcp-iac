from app.main import app

# AWS Lambda handler for FastMCP HTTP application
# FastMCP with stateless_http=True provides a Starlette/FastAPI compatible app
# that can be directly used as a Lambda handler
handler = app