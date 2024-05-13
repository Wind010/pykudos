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


### Generate new JWT secret key:
```sh
openssl rand -hex 32
```