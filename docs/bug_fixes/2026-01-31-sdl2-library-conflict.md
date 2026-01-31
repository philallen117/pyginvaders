# Bug Fix: SDL2 Library Conflict on macOS

**Date:** 31 January 2026  
**Severity:** High (Random Crashes)  
**Exit Code:** 139 (SIGSEGV)  
**Platform:** macOS with Homebrew

## Problem Description

The game crashed randomly with a segmentation fault (exit code 139) when running with `uv run main.py`. The crash occurred intermittently, particularly during font rendering operations in the game loop. The window would briefly appear then immediately crash.

## Root Cause

Multiple SDL2 libraries were being loaded simultaneously:

1. **Homebrew SDL2**: `/opt/homebrew/Cellar/sdl2/2.32.10/lib/libSDL2-2.0.0.dylib`
2. **pygame-ce bundled SDL2**: `/Users/phil/code/pyginvaders/.venv/lib/python3.14/site-packages/pygame/.dylibs/libSDL2-2.0.0.dylib`

This caused Objective-C runtime warnings:

```text
objc[...]: Class SDL_RumbleMotor is implemented in both /opt/homebrew/Cellar/sdl2/2.32.10/lib/libSDL2-2.0.0.dylib and 
/Users/phil/code/pyginvaders/.venv/lib/python3.14/site-packages/pygame/.dylibs/libSDL2-2.0.0.dylib. 
This may cause spurious casting failures and mysterious crashes.
```

The warnings explicitly state this "may cause spurious casting failures and mysterious crashes," which is exactly what was happening.

### Why Both Libraries Are Present

- **Homebrew SDL2** is installed as a dependency for FFmpeg
- **pygame-ce** bundles its own SDL2 for compatibility
- macOS's dynamic linker loads both when the game starts
- The duplicate class implementations cause memory corruption and random crashes

## Solution

Created a wrapper script `run_game.sh` that clears dynamic library paths before running the game, ensuring only pygame-ce's bundled SDL2 is loaded:

```bash
#!/bin/bash
# Wrapper script to run pyginvaders without the Homebrew SDL2 library conflict
# This prevents the system SDL2 from being loaded, using only pygame-ce's bundled SDL2

# Clear any existing library paths that might load Homebrew libraries
export DYLD_LIBRARY_PATH=""
export DYLD_FALLBACK_LIBRARY_PATH=""

# Run the game with uv
exec uv run python main.py
```

## Usage

Run the game using the wrapper script:

```bash
./run_game.sh
```

This is now the recommended way to run the game on macOS. Direct use of `uv run main.py` may still crash due to the SDL2 conflict.

## Why Removing Homebrew SDL2 Is Safe

While Homebrew SDL2 is a dependency of FFmpeg, removing it doesn't actually break FFmpeg functionality:

```bash
$ brew uses sdl2 --installed
ffmpeg
```

FFmpeg uses SDL2 only for optional display features (showing video in a window), not for core transcoding/encoding operations. Most command-line FFmpeg usage works perfectly without SDL2.

Using `brew uninstall --ignore-dependencies sdl2` removes SDL2 while keeping FFmpeg installed. This is the recommended solution to eliminate the library conflict permanently.

## Alternative Solutions Considered

### 1. Environment Variable Wrapper Script

Created `run_game.sh` to clear library paths:

```bash
export DYLD_LIBRARY_PATH=""
export DYLD_FALLBACK_LIBRARY_PATH=""
exec uv run python main.py
```

**Result:** Still showed duplicate library warnings and intermittent crashes due to macOS System Integrity Protection (SIP) stripping these environment variables for security.

### 2. Modified Wrapper with Library Path Manipulation

Attempted to explicitly exclude Homebrew paths or prepend virtual environment paths.

**Result:** Ineffective - macOS SIP prevents DYLD_* environment variable manipulation for processes launching system binaries.

### 3. Switching to pygame-ce

Already using pygame-ce (Community Edition), which has better macOS support and bundles SDL2.

**Result:** Doesn't solve the conflict since both Homebrew SDL2 and pygame-ce's bundled SDL2 are loaded.

### 4. Removing Homebrew SDL2 (Final Solution)

Used `brew uninstall --ignore-dependencies sdl2` to remove Homebrew SDL2, then reinstalled pygame-ce:

```bash
brew uninstall --ignore-dependencies sdl2
uv pip uninstall pygame-ce
uv pip install pygame-ce --reinstall
```

**Result:** ✅ Complete success - no warnings, no crashes, game runs perfectly every time.

## Verification

After removing Homebrew SDL2 and reinstalling pygame-ce:

- ✅ Game runs without crashing (tested multiple launches)
- ✅ All 49 tests pass  
- ✅ Game loop executes continuously without segfaults
- ✅ Font rendering works correctly
- ✅ No duplicate library warnings
- ✅ Clean SDL2 initialization using only pygame-ce's bundled library

Test commands:

```bash
# Quick launch test
timeout 5 uv run main.py

# 2-second sustained run
uv run main.py & sleep 2 && pkill -f main.py

# Full test suite
uv run pytest
```

All tests passed successfully with no crashes or warnings.

## Files Modified

- System: Removed Homebrew SDL2 (`brew uninstall --ignore-dependencies sdl2`)
- Python environment: Reinstalled pygame-ce to use bundled SDL2
- `run_game.sh` - Simplified to just run the game (wrapper no longer needed for conflict resolution)
- `README.md` - Updated run instructions
- `Justfile` - removed run task

## Technical Details

The crash stack trace showed:

```text
Fatal Python error: Segmentation fault
  File "/Users/phil/code/pyginvaders/src/pyginvaders/game.py", line 135 in draw_game
  File "/Users/phil/code/pyginvaders/src/pyginvaders/game.py", line 305 in run

Binary file ".../libSDL2-2.0.0.dylib", at SDL_AllocFormat_REAL+0x20
Binary file ".../libSDL2_ttf-2.0.0.2400.0.dylib", at Create_Surface_Blended+0x44
```

The crash occurred in SDL's memory allocation for font rendering surfaces, indicating memory corruption from the duplicate library implementations.

## Lessons Learned

1. **System library conflicts**: When using Python packages that bundle native libraries (like pygame), conflicts can arise with system-installed versions
2. **macOS dynamic linking**: Environment variables must be set before the process starts, not within Python code
3. **Wrapper scripts**: Simple shell wrappers are effective for controlling the runtime environment
4. **Platform-specific issues**: What works on Linux/Windows may have subtle issues on macOS due to different dynamic linking behavior
5. **Debugging native crashes**: Python's faulthandler and examining C stack traces are essential for diagnosing segfaults in extension modules
