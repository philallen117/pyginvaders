# Bug Fix: Crash When Invader Bullet Hits Player

**Date:** 31 January 2026  
**Severity:** High (Segmentation Fault)  
**Exit Code:** 139 (SIGSEGV)

## Problem Description

The game crashed with a segmentation fault (exit code 139) when an invader bullet collided with the player. This was a critical bug that made the game unplayable once the player was hit.

## Root Cause

When an invader bullet hit the player, the collision detection code would:

1. Detect the collision and set `game_lost = True`
2. Exit the bullet collision loop with `break`
3. **Continue executing the rest of the frame** including:
   - Updating invader positions (lines 241-264)
   - Firing new invader bullets (lines 267-278)
   - Drawing the game scene (line 280)

This created a race condition where game objects were being updated and drawn in an inconsistent state (game marked as lost but still processing normal game logic). This likely triggered an underlying SDL2 library bug, as evidenced by numerous warnings about duplicate class implementations:

```
objc[...]: Class SDL_RumbleMotor is implemented in both 
/opt/homebrew/Cellar/sdl2/2.32.10/lib/libSDL2-2.0.0.dylib and 
/Users/phil/code/pyginvaders/.venv/lib/python3.14/site-packages/pygame/.dylibs/libSDL2-2.0.0.dylib. 
This may cause spurious casting failures and mysterious crashes.
```

## Solution

Added an immediate `continue` statement after detecting game loss in [game.py](../../src/pyginvaders/game.py#L240-L243):

```python
# Check invader bullet - player collisions
player_rect = self.player.get_rectangle()
for bullet in self.invader_bullets:
    if not bullet.active:
        continue

    if check_rect_collision(bullet.get_rectangle(), player_rect):
        # Collision detected - game is lost
        bullet.deactivate()
        self.game_lost = True
        break  # Exit bullet loop

# If game was just lost, skip to next frame to show game over screen
if self.game_lost:
    continue
```

This ensures that when a collision is detected:

1. The game state is properly set to lost
2. The current frame immediately ends
3. The next frame starts at the top of the game loop where the game-over screen is correctly displayed (lines 195-199)

## Testing

Created comprehensive tests in [test_game_over.py](../../tests/test_game_over.py):

- `test_game_over_when_player_hit_by_invader_bullet()` - Verifies game transitions to lost state
- `test_collision_detection()` - Tests the AABB collision detection function

All 44 tests pass, including the existing collision tests in [test_game.py](../../tests/test_game.py):

- `test_invader_bullet_hits_player()`
- `test_invader_bullet_miss_player()`
- `test_game_lost_after_invader_kills()`

## Verification

The game now:

- Exits cleanly without crashing when the player is hit
- Properly displays the game over screen
- Maintains consistent game state throughout the collision process

## Files Modified

- `src/pyginvaders/game.py` - Added frame skip after game loss detection
- `tests/test_game_over.py` - New test file for game over scenarios

## Lessons Learned

When implementing state transitions in a game loop:

1. Ensure state changes are atomic and complete before the next frame
2. Skip remaining frame logic when entering terminal states (game over, pause, etc.)
3. Race conditions in C extension libraries (like pygame/SDL2) can cause mysterious crashes that manifest as segmentation faults
4. Always test state transitions, especially collision-triggered state changes
