Built with [FastAPI](https://fastapi.tiangolo.com/) framework.

### Run

Development
```sh
fastapi dev main.py
```


Production
```
fastapi run
```

### Environment Variables
Create a `.env` storing the environment variables for your configuration.

```sh
APP_NAME="PyKudos"
ADMIN_EMAIL="wind010@users.noreply.github.com"
SECRET_KEY=""
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_TYPE="in_memory"
DATABASE_CONNECTION_STRING=""
ENVIRONMENT='dev'
ALLOWED_HOSTS=["127.0.0.1", "test"]
ALLOWED_ORIGINS=["https://your_account.github.io/", "http://127.0.0.1:<YOUR_PORT>"]
SERVER_SIDE_RENDER=false
ENABLE_LOCAL_AUTH=false
ENABLE_GITHUB_AUTH=true
GITHUB_CLIENT_ID=""
GITHUB_CLIENT_SECRET=""
GITHUB_URL="https://github.com"
GITHUB_PAT=""
GITHUB_ORGS=[]
GITHUB_TEAMS=[]
```


### Generate new JWT secret key:
```sh
openssl rand -hex 32
```


## OAUTH

### Github
You will need to setup a new OAUTH application under your `github` account under `Settings` and `Developer Settings`.  

#### Server side rendered pages.
Use the `https://your.domain/auth/github/callback` for the `Authorization callback URL`.  The servers side set cookie will not be available to your client if they are hosted on different domains.

#### Using client side
Use location of client pages requires that the callback occur to one of your pages.  For example, `https://your.domain/login.html` for the `Authorization callback URL`.  The callback will then contain a `?code=<YOUR_CODE>` which is then used to retrieve the `access_token` with a separate `POST` call.  This way the `access_token` is used with all subsequent request calls. 


See [Authorizing OAuth Apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)



# Notes
* If the client page is on a different domain, you should add it to your `ALLOWED_ORIGINS` configuration.  
* When the OAUTH `access_token` is first obtained, you should have made the fetch request with the option: `credentials: "include"`.  See [fetch-credentials](https://developer.mozilla.org/en-US/docs/Web/API/fetch#credentials)

