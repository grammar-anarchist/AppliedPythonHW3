## Instructions to launch

1. Clone the repository: 

`git clone git@github.com:grammar-anarchist/AppliedPythonHW3.git`

2. Add a file `.env` of the following structure to the root of the repository:

```
DB_USER=postgres
DB_PASS=password
DB_HOST=db
DB_PORT=5432
DB_NAME=urls_project

REDIS_HOST=redis
REDIS_PORT=6379

JWT_SECRET_KEY=...
```

You have to create your own JWT secret key and add it to the corresponding field (e.g., you can generate it with `openssl rand -hex 32`).

3. Run `docker-compose up --build -d`

## Database description

There are 2 tables: `users` and `urls`.

- **users**  
  Stores user credentials, such as a unique `username`, `email` and a registration timestamp.

- **urls**
  Stores original URLs, their aliases and creation time. URLs created by authenticated users save the `user_id`. URLs are automatically deleted after a `redundant_period` number of days have passed (default 14), or if `expires_at` is set by the user.
  Usage information, such as `usage_count` (number of clicks) and `last_used_at` timestamp are also included.

## API description with examples

Examples below are given with Python httpx module.

```
import httpx

BASE_URL = "http://localhost:8000"
```

### Authorization

#### POST /auth/register

Register in the app by inserting a unique username, email (must be valid in form) and password. 

```
with httpx.Client() as client:
    response = client.post(f"{BASE_URL}/auth/register", json={
        "username": "test",
        "email": "valid@email.com",
        "password": pass
    })
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())
```

#### POST /auth/token

Generates an access token. The user must be registered to use this endpoint.

Authentication basically sums up to providing this access token to an endpoint.

No need for it in Swagger UI: instead, after `/auth/register` you should use the `Authorize` button in the top right.

```
with httpx.Client() as client:
    response = client.post(f"{BASE_URL}/auth/token",
        data=d{
            "username": "test",
            "password": "password",
            "grant_type": "password",
            "scope": "",
            "client_id": "",
            "client_secret": ""
        }, 
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())
    access_token = response.json()["access_token"]
```

#### POST /auth/me

