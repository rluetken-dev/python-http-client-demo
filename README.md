# Demo HTTP Client
![CI](https://github.com/rluetken-dev/demo/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)

Practice project: a simple Python CLI tool that makes HTTP requests, 
supports retries, and shows colored output for success and errors. 

## Installation
Clone the repository and install dependencies:

```bash
git clone git@github.com:rluetken-dev/demo.git
cd demo
python -m venv .venv
source .venv/bin/activate   # on Linux/Mac
# .venv\Scripts\activate    # on Windows
pip install -r requirements.txt
```

## Features
- GET requests with JSON response
- Automatic retries on errors (503, 500, etc.)
- Colored output (green = success, red = error)
- Configurable URL and timeout via CLI arguments

## Usage
```bash
python demo.py --url https://httpbin.org/uuid
python demo.py --url https://jsonplaceholder.typicode.com/todos/1 -t 3
```




