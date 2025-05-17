# API Test Suite

The included tests start the Flask application locally and send HTTP requests to every endpoint. Each API call is validated separately to ensure that responses and status codes match expectations.

Run the suite with `pytest` from the repository root. The server is started using Werkzeug's test server in a background thread and is automatically shut down when tests complete.

## Endpoints verified

- `/hello` returns a welcome message.
- `/submit` accepts JSON data and echoes the input.
- `/version` reports the application version.
- `/sysinfo` provides system information.
- `/log` returns generated log text.
- `/check_user` authenticates valid and invalid users.
