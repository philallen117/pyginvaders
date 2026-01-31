#!/bin/bash
# Wrapper script to run pyginvaders without the Homebrew SDL2 library conflict
# This prevents the system SDL2 from being loaded, using only pygame-ce's bundled SDL2

# Clear any existing library paths that might load Homebrew libraries
export DYLD_LIBRARY_PATH=""
export DYLD_FALLBACK_LIBRARY_PATH=""

# Run the game with uv
exec uv run python main.py
