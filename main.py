from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from utils import verify_jwt

class PolicyRequest(BaseModel):
    name: str
    phone: str
    premium: float
    suminsured: float

class Message(BaseModel):
    message: str

token_auth_scheme = HTTPBearer()

# Creates app instance
app = FastAPI()

@app.get("/")
def hello_world() -> Message:
    """Hello world endpoint"""
    return {
        "message": "Hello from team Etherisc!"
    }


@app.post("/")
@verify_jwt
def create_policy(request: PolicyRequest, response: Response, token: str = Depends(token_auth_scheme)) -> Message:
    """Create policy endpoint"""
    print(request)
    return {
        "message": "Policy created for %s!" % request.name
    }
