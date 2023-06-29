from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from utils import verify_jwt_with_scope

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
# @verify_jwt
@verify_jwt_with_scope("write:policy")
def create_policy(request: PolicyRequest, response: Response, token: str = Depends(token_auth_scheme)) -> Message:
    """Create policy endpoint"""
    print(request)

    if request.name.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty")
    if request.phone.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone cannot be empty")
    if request.premium <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Premium must be greater than 0")
    if request.suminsured <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sum insured must be greater than 0")
    if request.premium > request.suminsured:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Premium cannot be greater than sum insured")

    return {
        "message": "Policy created for %s!" % request.name
    }
