# Python HTTP Client Demo

[![CI](https://img.shields.io/github/actions/workflow/status/rluetken-dev/python-http-client-demo/ci.yml?branch=main&event=push&label=CI)](https://github.com/rluetken-dev/python-http-client-demo/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Imports: isort](https://img.shields.io/badge/imports-isort-ef8336.svg)
![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
[![Release](https://img.shields.io/github/v/release/rluetken-dev/python-http-client-demo?sort=semver&display_name=tag)](https://github.com/rluetken-dev/python-http-client-demo/releases)

A small Python CLI and library for making HTTP requests with `httpx`.

The project demonstrates clean package structure, deterministic tests, retry handling, CLI usage, formatting, linting, security checks, and GitHub Actions CI.

## Features

- HTTP client wrapper based on `httpx`
- CLI entry point through `python -m demo_client`
- GET and POST helper methods
- JSON and plain-text response handling
- Retry handling for transient HTTP and transport failures
- Unit tests with mocked HTTP calls
- Formatting with Black
- Import sorting with isort
- Linting with Flake8
- Security scanning with Bandit
- GitHub Actions CI
- Conventional commit guidelines

## Tech Stack

- Python 3.12+
- httpx
- pytest
- respx
- Black
- isort
- Flake8
- Bandit
- Safety
- pre-commit
- GitHub Actions

## Getting Started

### Prerequisites

- Python 3.12 or newer
- Git

### Clone

```powershell
git clone https://github.com/rluetken-dev/python-http-client-demo.git
cd python-http-client-demo
```

### Create A Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS, Linux, or WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```powershell
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

### Install Git Hooks

```powershell
pre-commit install
```

## CLI Usage

Show help:

```powershell
python -m demo_client --help
```

Run a demo request:

```powershell
python -m demo_client --url https://httpbin.org/get
```

Set a custom timeout:

```powershell
python -m demo_client --url https://httpbin.org/get --timeout 10
```

The CLI prints formatted JSON and exits without writing local files.

## Library Usage

```python
from demo_client import DemoClient

with DemoClient("https://api.example.com", timeout=5.0) as client:
    data = client.get("/items")
    print(data)
```

Convenience helper:

```python
from demo_client import fetch_url

result = fetch_url("https://httpbin.org/get", timeout=5.0)
print(result)
```

## Tests And Checks

Run the test suite:

```powershell
pytest
```

Run formatting and lint checks:

```powershell
black --check .
isort --check-only .
flake8
```

Run security checks:

```powershell
bandit -r src -x tests
safety check
```

Run the configured pre-commit hooks:

```powershell
pre-commit run --all-files
```

## Project Structure

```text
python-http-client-demo/
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ src/
│  └─ demo_client/
│     ├─ __init__.py
│     └─ __main__.py
├─ tests/
├─ COMMITS.md
├─ pyproject.toml
├─ pytest.ini
├─ requirements.txt
└─ README.md
```

## CI

GitHub Actions runs the project checks on pushes and pull requests to `main`.

The CI workflow installs the package with development dependencies, runs pre-commit checks, executes the test suite with coverage, and runs security scans.

## Development Notes

- Keep network-facing code small and easy to test.
- Mock external HTTP calls in tests instead of relying on live services.
- Keep CLI behavior thin and delegate request logic to the package.
- Use Conventional Commits for a readable release history.

See [COMMITS.md](./COMMITS.md) for commit message guidelines.

## Releases

This repository uses semantic version tags in the format `vX.Y.Z`.

Release notes should summarize user-visible changes, quality improvements, and validation results.

## License

This project is released under the MIT License.
