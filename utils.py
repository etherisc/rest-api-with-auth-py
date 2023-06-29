import os
from fastapi import HTTPException
import jwt
import functools
from configparser import ConfigParser

def verify_jwt(func):
    """Sleep 1 second before calling the function"""
    @functools.wraps(func)
    def wrapper_verify_jwt(*args, **kwargs):
        token = kwargs['token']
        jwt_verify_result = TokenHelper(token.credentials).verify()
        if jwt_verify_result.get("status"):
            print("JWT invalid")
            raise HTTPException(status_code=401, detail=jwt_verify_result.get("message"))
        return func(*args, **kwargs)
    return wrapper_verify_jwt

def verify_jwt(*expected_scopes):
    def require_scope_actual(func):
        """Sleep 1 second before calling the function"""
        @functools.wraps(func)
        def wrapper_require_scope(*args, **kwargs):
            token = kwargs['token']
            jwt_verify_result = TokenHelper(token.credentials).has_scopes(*expected_scopes)
            if jwt_verify_result.get("status"):
                print("scope invalid")
                raise HTTPException(status_code=403, detail=jwt_verify_result.get("message"))
            return func(*args, **kwargs)
        return wrapper_require_scope
    return require_scope_actual


def set_up():
    """Sets up configuration for the app"""

    env = os.getenv("ENV", ".config")

    if env == ".config":
        config = ConfigParser()
        config.read(".config")
        config = config["AUTH0"]
    else:
        config = {
            "DOMAIN": os.getenv("DOMAIN", "your.domain.com"),
            "API_AUDIENCE": os.getenv("API_AUDIENCE", "your.audience.com"),
            "ISSUER": os.getenv("ISSUER", "https://your.domain.com/"),
            "ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
        }
    return config


class TokenHelper():
    """Does all the token verification using PyJWT"""

    def __init__(self, token):
        self.token = token
        self.config = set_up()

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        print("JWT payload: %s" % payload)
        return payload
    
    def has_scopes(self, *expected_scopes):
        payload = self.verify()
        scope = payload.get("scope", "")
        if len(expected_scopes) == 0:
            return {}
        if scope == "":
            return {"status": "error", "message": "Invalid scope"}
        token_scopes = scope.split(" ")
        # print("Token scopes: %s" % token_scopes)
        # print ("Expected scopes: %s" % expected_scopes)
        for expected_scope in expected_scopes:
            if expected_scope not in token_scopes:
                return {"status": "error", "message": "Invalid scope"}
        return {}
    