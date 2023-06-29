# rest-api-with-auth-py in python

## Run

```bash
uvicorn main:app --reload
```

## Run in container

```bash
docker build -t rest-api-with-auth-py .

docker run --rm=true -p 8000:8000 --env-file=.config -e ENV=prod rest-api-with-auth-py
```

## Environment variables

Set according to your Auth0 account

```bash
# .config
DOMAIN=
API_AUDIENCE=
ALGORITHMS=RS256
ISSUER=
```

## API Endpoints

### GET /

Returns a welcome message.

### POST /

Create a new policy. Provide the following parameters in the request body:

```json
{
  "name": "policy holder name",
  "phone": "phone number",
  "premium": "premium amount",
  "suminsured": "sum insured amount" 
}
```

This must be sent as an authenticated request. The JWT token must be sent in the Authorization header as a Bearer token.
The JWT token must be valid, have scope `write:policy` and the audience must be as configured in the environment variable `AUTH0_AUDIENCE`.
