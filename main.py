from fastapi import FastAPI, Depends, Response, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from utils import VerifyToken

token_auth_scheme = HTTPBearer()

# Creates app instance
app = FastAPI()


class PolicyRequest(BaseModel):
    name: str
    phone: str
    premium: float
    suminsured: float

class Message(BaseModel):
    message: str


@app.get("/")
def hello_world() -> Message:
    """Hello world endpoint"""

    return {
        "message": "Hello from team Etherisc!"
    }


@app.post("/")
def create_policy(request: PolicyRequest, response: Response, token: str = Depends(token_auth_scheme)) -> Message:
    """Create policy endpoint"""

    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    
    # print request body
    print(request)

    return {
        "message": "Policy created for %s!" % request.name
    }
