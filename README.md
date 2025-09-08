# Demo HTTP Client (Python)

![CI](https://github.com/rluetken-dev/python-http-client-demo/actions/workflows/ci.yml/badge.svg?branch=master)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Imports: isort](https://img.shields.io/badge/imports-isort-ef8336.svg)
![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow.svg)
![Vuln DB: Safety](https://img.shields.io/badge/vulnerabilities-safety-red.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

A small **Python CLI & library** for practicing clean code, packaging, and CI/CD.  
Includes formatting, linting, security checks, and unit tests.

---

## ✨ Features
- Simple CLI entrypoint (HTTP requests demo)
- Strict formatting & linting (Black, isort, Flake8)
- Security scanning (Bandit / Safety)
- GitHub Actions CI (style, tests on push)
- Pre-commit hooks

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- (recommended) virtualenv

### Quickstart
```bash
git clone https://github.com/rluetken-dev/python-http-client-demo.git
cd python-http-client-demo

# Create & activate virtualenv
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .\.venv\Scripts\Activate.ps1

# Install deps
pip install -U pip
pip install -e ".[dev]"

# Install git hooks
pre-commit install
```

### Run
```bash
# CLI usage
python -m demo_client --help
python -m demo_client get https://httpbin.org/get
```

### Test & Quality
```bash
pytest -q
pre-commit run --all-files
```

---

## 🧱 Tech Stack
- Python 3.12, requests/httpx (depending on your final choice)
- Pytest, coverage, pre-commit
- GitHub Actions (CI)

---

## 📂 Project Structure
```
python-http-client-demo/
├─ src/demo_client/
│  ├─ __init__.py
│  └─ __main__.py  # Entry point für `python -m demo_client`
├─ tests/
├─ commits.md
├─ pyproject.toml
└─ README.md
```

---

## 💡 Development Tips
- Keep network code thin and pure; isolate side-effects.
- Enforce formatting & linting via pre-commit.
- Fail CI on style or security regressions.
- See [COMMITS.md](./COMMITS.md) for Conventional Commits guidelines.

---

## 🧭 Roadmap
- [ ] Publish package to TestPyPI
- [ ] Add type hints and mypy
- [ ] Add richer CLI (subcommands) and config file

---

## 📜 License
This project is released under the **MIT License**.
