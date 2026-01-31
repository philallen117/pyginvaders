# README

## Purpose

This project is a simple Space Invaders clone, using pygame, for learning and language contrast purposes.

It is inspired by the ZigInvaders course created by Brad Cypert.

## Project set-up

`uv` is the package manager and Python manager for this project.

The formatter is `black`.

The linter is `flake8`.

The type checker is `pyrefly`.

The test runner is `pytest`.

`main` should be run with `./run_game.sh` (recommended to avoid SDL2 library conflicts on macOS) or `uv run main.py`.

## Workflow

When setting up for development, in the root folder run `uv pip install -e .` once initially to install the package in editable mode. The -e (editable) flag creates a link to your source directory, so changes to your .py files are automatically picked up without reinstalling. After that:

Don't need to reinstall:

- When editing existing Python files (changes are immediately available)
- When adding/modifying code in existing modules

Do need to reinstall:

- When you modify pyproject.toml (dependencies, metadata, etc.)
- When you add new top-level packages or modules to the src structure
- When you change entry points or package configuration
