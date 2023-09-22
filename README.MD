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


## Initial instance setup

```
# create dokku application 
dokku apps:create wfp-api

# add new domain and remove default domain
dokku domains:add wfp-api api.wfp.etherisc.com
dokku domains:remove wfp-api wfp-api.wfp.etherisc.com

# set correct proxy ports for http and https
dokku ports:add wfp-api https:443:8000
dokku ports:add wfp-api http:80:8000

# create mongo service
dokku mongo:create mongo-wfp-api

# link the mongo service to the app
dokku mongo:link mongo-wfp-api wfp-api

# now push deployment via git 
# 1. add new git remote 'git remote add dokku dokku@<host>:wfp-api'
# 2. 'git push dokku master:main'

# enable let's encrypt for https certificates
dokku letsencrypt:enable wfp-api

# app should be ready now - open in browser
```

### Dokku mongo debug connection

Example using service _mongo-wfp-api_:

1. Expose mongo port on dokku `dokku mongo:expose mongo-wfp-api`
1. Find the exposed port in the output above or via `dokku mongo:info mongo-wfp-api`
1. Open ssh tunnel with dokku mongo port forward `ssh -L 6479:localhost:15956 user@host`
1. Now connect with mongo client of choice using `localhost:6479` as host and the password mentioned in mongo info
1. When finished, close the ssh tunnel by logging out of the ssh shell and unexpose the mongo port `dokku mongo:unexpose mongo-wfp-api`

