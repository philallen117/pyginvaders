default:
    @just --list

test: lint typecheck unittest

lint:
    @echo "Running flake8 ..."
    @if command -v uv run flake8 >/dev/null 2>&1; then \
        uv run flake8; \
    else \
        echo "flake8 not found"; \
    fi

typecheck:
    @echo "Running pyrefly ..."
    @if command -v uv run pyrefly >/dev/null 2>&1; then \
        uv run pyrefly check .; \
    else \
        echo "pyrefly not found"; \
    fi

unittest:
    @echo "Running pytest ..."
    @if command -v uv run pytest >/dev/null 2>&1; then \
        uv run pytest -v; \
    else \
        echo "pytest not found"; \
    fi

install-dev:
    @echo "Installing pyginvaders for development ..."
    @if command -v uv >/dev/null 2>&1; then \
        uv pip install -e .; \
    else \
        echo "uv not found"; \
    fi
