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

  Stores original URLs and corresponding aliases. URLs created by authenticated users save the `user_id`. URLs are automatically deleted after a `redundant_period` number of days have passed (default 14), or if `expires_at` is set by the user.
  Usage information, such as `usage_count` (number of clicks) and `last_used_at` timestamp are also included.

## API description with examples

Examples below are given with Python httpx module.

```
import httpx

BASE_URL = "http://localhost:8000"

with httpx.Client() as client:
    response = ...
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())
```

### Authorization

#### POST /auth/register

Register in the app by inserting a unique username, email (must be valid in form) and password. 

```
response = client.post(f"{BASE_URL}/auth/register", json={
    "username": "test",
    "email": "valid@email.com",
    "password": pass
})
```

#### POST /auth/token

Generates an access token. The user must be registered to use this endpoint.

Authentication basically sums up to providing this access token to an endpoint.

No need for it in Swagger UI: instead, after `/auth/register` you should use the `Authorize` button in the top right.

```
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
access_token = response['access_token']
```

#### POST /auth/me

Returns information about the user, including username, email and registration timestamp.

User must be authenticated to make request, i.e. provide the access token.

```
response = client.get(f"{BASE_URL}/auth/me", 
    headers={
        "Authorization": f"Bearer {access_token}"
    }
)
```

### URL shortening

#### POST /links/shorten

Allows to create a short link for the given url `original_url`. If a custom alias is not provided, uses the database id of the url as the alias. Then you can access the link by making a request `GET /links/{short_code}` (see below).

If `expires_at` is provided, creates a background task to delete the link at a given timestamp. If timestamp is given without timezone, assumes UTC.

If `redundant_period` is provided, the link will be deleted after `redundant_period` number of days after its last use/creation. If not provided, set to 14.

If user is authenticated, matches the url with the user's id.

The request returns the short code.

```
response = client.post(f"{BASE_URL}/links/shorten",
    json={
        "original_url": "https://example.com/",
        "alias": "example",
        "expires_at": "2025-04-25T21:00:00+03:00",
        # "redundant_period": 14
    },
    headers={
        "Authorization": f"Bearer {access_token}"
    }
)
tiny_url = response['short_code']
```

#### GET /links/{short_code}

Returns a redirect response for the original URL.

Easiest to see by typing `f"{BASE_URL}/links{short_code}` in a browser.

#### GET /links/search

Allows to get all the short codes that refer to the given original URL.

```
response = client.get(f"{BASE_URL}/links/search",
    params={
        "original_url": "https://example.com/"
    }
)
tiny_urls = response['tiny_urls']
```

#### GET /links/{short_code}/stats

Allows to get basic statistics for the given short code: number of clicks, timestamp of creation and last usage, original URL. Authentication is not required.

```
response = client.get(f"{BASE_URL}/links/{short_code}/stats")
```

#### DELETE /links/{short_code}

Allows to delete the URL from the database. The user must be authenticated. The user making the request must be the same as the creator of the short code.

Returns a response with a confirmation.

```
response = client.delete(f"{BASE_URL}/links/{short_code}"
        headers={
            "Authorization": f"Bearer {access_token}"
        }
)
```

#### PUT /links/{short_code}

Allows to change the original URL to a new one. Usage statistics are not renewed: it is assumed that they are calculated for the short code. The user must be authenticated. The user making the request must be the same as the creator of the short code.

Returns a response with a confirmation.

```
response = client.put(f"{BASE_URL}/links/{short_code}",
        json={
            "new_url": "https://github.com/"  
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
)
```
