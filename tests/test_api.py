"""Integration tests for the Flask API.

The Flask app is started locally using ``werkzeug.serving.make_server``. Tests
send HTTP requests to this server to verify each endpoint individually. A
module-scoped fixture ensures that the server is started once and shut down when
all tests finish.
"""

import threading
import time
import requests
import pytest
from werkzeug.serving import make_server
from app import app

class ServerThread(threading.Thread):
    """Background thread running the Flask development server."""
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
        self.ctx.pop()

@pytest.fixture(scope="module")
def test_server():
    """Start the server for the duration of the test module."""
    server = ServerThread()
    server.start()
    # Give the server a moment to bind to the port
    time.sleep(1)
    yield
    server.shutdown()


def test_hello_endpoint(test_server):
    """Verify that /hello returns the default greeting."""
    resp = requests.get('http://127.0.0.1:5000/hello')
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello, World!"}


def test_submit_endpoint(test_server):
    """Ensure POST /submit echoes provided JSON."""
    payload = {"input_field_1": "foo", "input_field_2": "bar", "language": "en"}
    resp = requests.post('http://127.0.0.1:5000/submit', json=payload)
    assert resp.status_code == 200
    assert resp.json().get('status') == 'success'


def test_version_endpoint(test_server):
    """Check that /version reports an app version."""
    resp = requests.get('http://127.0.0.1:5000/version')
    assert resp.status_code == 200
    assert 'version' in resp.json()


def test_sysinfo_endpoint(test_server):
    """Confirm /sysinfo returns basic system data."""
    resp = requests.get('http://127.0.0.1:5000/sysinfo')
    assert resp.status_code == 200
    body = resp.json()
    assert 'platform' in body
    assert 'system' in body
    assert 'version' in body


def test_log_endpoint(test_server):
    """Ensure /log returns log text and HTTP 200."""
    resp = requests.get('http://127.0.0.1:5000/log')
    assert resp.status_code == 200
    assert resp.text


def test_check_user_success(test_server):
    """Valid user should authenticate successfully."""
    resp = requests.post('http://127.0.0.1:5000/check_user', data={'user': 'nik'})
    assert resp.status_code == 200
    assert resp.json().get('auth') == 'pass'


def test_check_user_fail(test_server):
    """Invalid user should return error status."""
    resp = requests.post('http://127.0.0.1:5000/check_user', data={'user': 'other'})
    assert resp.status_code == 500
    assert resp.json().get('auth') == 'FAILED'
