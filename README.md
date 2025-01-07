# Food Repo User API v2
API to manage users of a front end application that consumes an external meal recipe API.

## Endpoints

All endpoints except `POST /users` require authentication via the session token `X-Session-Token`, which will be included in the request's header.

POST parameters are sent as form-data.

|Method|Endpoint|POST params|
|------|--------|-----------|
|POST|/users|email, first_name, last_name, password|
|POST|/auth/login|email, password|
|DELETE|/auth/logout||
|GET|/users/<user_id>/favourites||
|POST|/users/<user_id>/favourites|recipe_id|
|DELETE|/users/<user_id>/favourites|recipe_id|

Return values:

- POST /users
```json
{
    "user_id": <value>
}
```
```json
{
    "error": "Incorrect parameters"
}
```
- POST /validation
```json
{
    "user_id": <value>
}
```
```json
{
    "error": "Incorrect password"
}
```
```json
{
    "error": "The user does not exist"
}
```
- GET /users/<user_id>/favourites
```json
{
    "recipes": [
        {
            "recipe_id": <value>
        }
    ]
}
```
- POST /users/<user_id>/favourites
```json
{
    "status": "ok"
}
```
- DELETE /users/<user_id>/favourites
```json
{
    "status": "ok"
}
```

## Installation

#### Option 1. Docker
1. Start Docker Desktop
2. In the command line, run `docker-compose up -d`. The API will be available at `http://localhost:5510`.

#### Option 2. Manual
Python 3.4 or higher required.

1. Create a virtual environment:
```
python -m venv venv
```

2. Activate the virtual environment.
- Windows cmd: `.\venv\Scripts\activate`
- Windows Powershell: `.\venv\Scripts\Activate`
- Linux and Mac: `source venv/bin/activate`

3. Install dependencies:
```
pip install -r requirements.txt
```

4. The first time the API is run, create the database:
```
python -m flask --app food_repo_users init-db
```

## Running the API
Within (venv), run:
```
python -m flask --app food_repo_users run --port 5510 --debug
```
The endpoints will be available at `http://localhost:5510`.

## Tools
SQLite / Flask / Python

## Author
Arturo Mora-Rioja