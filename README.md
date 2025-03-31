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
