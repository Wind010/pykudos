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
ALLOWED_HOSTS=["localhost","test"]
```


### Generate new JWT secret key:
```sh
openssl rand -hex 32
```