# Contributing to Price Intelligence System

Thank you for your interest in contributing to the Price Intelligence System! We welcome all contributions, including bug reports, feature requests, documentation improvements, and code contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [License](#license)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Configure** the remote upstream:
   ```bash
   git remote add upstream https://github.com/yourusername/Real_Time_Price_Intelligence_System.git
   ```
4. Create a new **branch** for your changes

## Development Environment Setup

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- MySQL 8.0+ or PostgreSQL 13+
- Redis (for caching and rate limiting)
- Git

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Real_Time_Price_Intelligence_System.git
   cd Real_Time_Price_Intelligence_System
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update the variables in `.env` with your local configuration

5. **Initialize the database**:
   ```bash
   python -m api.db.init_db
   ```

6. **Run database migrations** (if any):
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**:
   ```bash
   uvicorn api.main:app --reload
   ```

## Project Structure

```
Real_Time_Price_Intelligence_System/
├── api/                         # Main API package
│   ├── config/                  # Configuration files
│   ├── db/                      # Database models and migrations
│   ├── models/                  # SQLAlchemy models
│   ├── routers/                 # API route handlers
│   ├── schemas/                 # Pydantic models
│   ├── services/                # Business logic
│   ├── utils/                   # Utility functions
│   ├── main.py                  # FastAPI application
│   └── __init__.py
├── tests/                       # Test files
├── alembic/                     # Database migrations
├── .env.example                 # Example environment variables
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml
```

## Making Changes

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-short-description
   ```

2. **Make your changes** following the code style guidelines

3. **Run tests** to ensure nothing is broken:
   ```bash
   pytest
   ```

4. **Commit your changes** with a descriptive message:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   # or
   git commit -m "fix: resolve issue with X"
   ```

5. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

6. **Open a Pull Request** against the `main` branch

## Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **Mypy** for type checking
- **isort** for import sorting

Before committing, run:

```bash
black .
flake8
mypy .
isort .
```

## Testing

We use `pytest` for testing. To run the test suite:

```bash
pytest
```

For test coverage report:

```bash
pytest --cov=api --cov-report=term-missing
```

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, including new environment variables, exposed ports, useful file locations, and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. The PR must pass all CI/CD checks before it can be merged.
5. The PR must be reviewed and approved by at least one maintainer.

## Reporting Issues

When reporting issues, please include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Any relevant error messages or logs
- Your environment details (OS, Python version, etc.)

## License

By contributing, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE) file.
