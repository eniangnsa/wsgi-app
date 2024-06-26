# Time Zone Service

This project is a WSGI application that provides functionalities similar to the service provided by time.is. It allows users to get the current time in a specified time zone, convert dates and times between different time zones, and calculate the difference in seconds between two dates in different time zones.

## Features

1. **Get Current Time**: 
    - `GET /<tz name>`: Returns the current time in the specified time zone in HTML format. If `<tz name>` is empty, it defaults to GMT.

2. **Convert Time Between Time Zones**: 
    - `POST /api/v1/convert`: Converts date/time from one time zone to another.
    - Request JSON: `{"date": "12.20.2021 22:21:05", "tz": "EST", "target_tz": "Europe/London"}`

3. **Calculate Date Difference**:
    - `POST /api/v1/datediff`: Returns the number of seconds between two dates in different time zones.
    - Request JSON: `{"first_date":"12.06.2024 22:21:05", "first_tz": "EST", "second_date":"12:30pm 2024-02-01", "second_tz": "Europe/Moscow"}`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/eniangnsa/wsgi-app.git
    cd time_service
    ```

2. Install the required packages:
    ```sh
    pip install pytz
    ```

## Running the Application

1. Run the application using the built-in WSGI server:
    ```sh
    python app.py
    ```

2. The server will start on `localhost` at port `8000`.

## Endpoints and Usage

### Get Current Time

- **Endpoint**: `GET /<tz name>`
- **Description**: Returns the current time in the specified time zone in HTML format. If `<tz name>` is empty, it defaults to GMT.
- **Example**: 
    ```sh
    curl http://localhost:8000/Europe/London
    ```

### Convert Time Between Time Zones

- **Endpoint**: `POST /api/v1/convert`
- **Description**: Converts date/time from one time zone to another.
- **Request Body**:
    ```json
    {
        "date": "12.20.2021 22:21:05",
        "tz": "EST",
        "target_tz": "Europe/London"
    }
    ```
- **Example**: 
    ```sh
    curl -X POST http://localhost:8000/api/v1/convert -H "Content-Type: application/json" -d '{"date":"12.20.2021 22:21:05", "tz": "EST", "target_tz": "Europe/London"}'
    ```

### Calculate Date Difference

- **Endpoint**: `POST /api/v1/datediff`
- **Description**: Returns the number of seconds between two dates in different time zones.
- **Request Body**:
    ```json
    {
        "first_date":"12.06.2024 22:21:05",
        "first_tz": "EST",
        "second_date":"12:30pm 2024-02-01",
        "second_tz": "Europe/Moscow"
    }
    ```
- **Example**: 
    ```sh
    curl -X POST http://localhost:8000/api/v1/datediff -H "Content-Type: application/json" -d '{"first_date":"12.06.2024 22:21:05", "first_tz": "EST", "second_date":"12:30pm 2024-02-01", "second_tz": "Europe/Moscow"}'
    ```

## Testing

You can use `curl` commands or Postman to test the endpoints.

### Using Postman

1. **GET Request**
    - Method: GET
    - URL: `http://localhost:8000/Europe/London`

2. **POST Request to `/api/v1/convert`**
    - Method: POST
    - URL: `http://localhost:8000/api/v1/convert`
    - Body (raw JSON):
        ```json
        {
            "date": "12.20.2021 22:21:05",
            "tz": "EST",
            "target_tz": "Europe/London"
        }
        ```

3. **POST Request to `/api/v1/datediff`**
    - Method: POST
    - URL: `http://localhost:8000/api/v1/datediff`
    - Body (raw JSON):
        ```json
        {
            "first_date": "12.06.2024 22:21:05",
            "first_tz": "EST",
            "second_date": "12:30pm 2024-02-01",
            "second_tz": "Europe/Moscow"
        }
        ```

