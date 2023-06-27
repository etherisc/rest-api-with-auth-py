"""main.py
Python FastAPI Auth0 integration example
"""

from fastapi import FastAPI
from pydantic import BaseModel


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
def create_policy(request: PolicyRequest) -> Message:
    """Create policy endpoint"""
    # print request body
    print(request)

    return {
        "message": "Policy created for %s!" % request.name
    }
