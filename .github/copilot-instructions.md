# Copilot Instructions

## Project Overview

This is a Python project - a Space Invaders clone using pygame for learning purposes.

## Development Tools

- **Package Manager**: `uv` - use `uv run` to execute scripts, `uv add` to add dependencies
- **Formatter**: `black` - all Python code should follow black's formatting standards
- **Linter**: `flake8` - code should pass flake8 checks
- **Type Checker**: `pyrefly` - provide type hints where appropriate

## Python Guidelines

- Write clean, readable Python code following PEP 8 conventions
- Use type hints for function signatures and class attributes
- Keep functions focused and single-purpose
- Write docstrings for classes and non-trivial functions
- Prefer explicit over implicit code
- Use meaningful variable and function names

## Running the Project

Execute the main program with:
```bash
uv run main.py
```

## Code Style

- Use black formatting (line length 88 characters by default)
- Follow flake8 linting rules
- Add type annotations for better code clarity and pyrefly compatibility
- Use pytest to run tests

## Workflow

This project has run `uv pip install -e .` to install the `pyginvaders` package in editable mode. The -e (editable) flag creates a link to the source directory, so changes to .py files are automatically picked up without reinstalling. After that:

Don't need to reinstall:

- When editing existing Python files (changes are immediately available)
- When adding/modifying code in existing modules

Do need to reinstall:

- When you modify pyproject.toml (dependencies, metadata, etc.)
- When you add new top-level packages or modules to the src structure
- When you change entry points or package configuration
