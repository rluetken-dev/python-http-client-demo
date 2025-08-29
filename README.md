# Demo HTTP Client

Practice project: a simple Python CLI tool that makes HTTP requests, 
supports retries, and shows colored output for success and errors. 

## Features
- GET requests with JSON response
- Automatic retries on errors (503, 500, etc.)
- Colored output (green = success, red = error)
- Configurable URL and timeout via CLI arguments

## Usage
```bash
python demo.py --url https://httpbin.org/uuid
python demo.py --url https://jsonplaceholder.typicode.com/todos/1 -t 3
