#!/bin/bash
# Wrapper script to run pyginvaders
# 
# Note: If you experience crashes with duplicate SDL2 library warnings,
# the most reliable fix is to uninstall Homebrew SDL2:
#   brew uninstall sdl2
#
# This may require reinstalling ffmpeg if you use it:
#   brew reinstall ffmpeg
# (ffmpeg will work fine for most tasks without SDL2)

# Run the game with uv
uv run python main.py
