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

```
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

## Why We Can't Just Remove Homebrew SDL2

The Homebrew SDL2 library is required by FFmpeg:

```bash
$ brew uses sdl2 --installed
ffmpeg
```

Removing the Homebrew SDL2 would break FFmpeg, which may be used by other tools and applications on the system.

## Alternative Solutions Considered

### 1. Environment Variable in main.py

Setting `DYLD_LIBRARY_PATH` or `DYLD_FALLBACK_LIBRARY_PATH` inside Python code doesn't work because the dynamic linker has already loaded libraries by the time Python imports pygame.

### 2. Switching to pygame-ce

Already using pygame-ce (Community Edition), which has better macOS support than standard pygame, but the conflict still occurs because both bundle SDL2 and Homebrew SDL2 is in the system path.

### 3. Removing Homebrew SDL2

Not viable due to FFmpeg dependency.

## Verification

After implementing the wrapper script:

- ✅ Game runs without crashing
- ✅ All 49 tests pass  
- ✅ Game loop executes continuously without segfaults
- ✅ Font rendering works correctly
- ⚠️  Warnings still appear but don't cause crashes

## Files Modified

- `run_game.sh` - New wrapper script (executable)
- `README.md` - Updated to recommend using wrapper script

## Technical Details

The crash stack trace showed:

```
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
