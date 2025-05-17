# Performance Test API

A small Flask application created mainly for performance testing.

## Setup

1. Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Start the application:

```bash
python app.py
```

The file `perf_for_devs.jmx` contains a JMeter script that can be used to load test this service.

## Running API tests

1. Install the dependencies listed in `requirements.txt` if you have not done so:

```bash
pip install -r requirements.txt
```

2. Execute the test suite with `pytest`:

```bash
pytest
```

The command starts the Flask server locally and runs a set of API verification calls. Results for each endpoint are displayed in the test output.
