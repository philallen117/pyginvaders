Now, we will allow the Player to fire PlayerBullets.

- When the human player presses the space bar, a bullet is fired from the Player object. Note that holding the space bar down should cause a continuous stream of fire; the human player needs to press the space bar once for each bullet.
- The game logic takes an inactive bullet from the pool, if one is available. (Order does not matter.) If no bullets are currently inactive, nothing further happens. This is not an error condition.
- The chosen bullet is placed immediately above the Player object and horizontally centred on the Player object.
- In each frame, the game should display all active bullets.

Plan these changes, and for unit tests that cover the logic of firing, to include the case where the pool is exhausted and nothing further happens.

---

There is a bug in pyginvaders/game.py around line 43 - the bullets must start from the top of the Player object, but they are appearing within the player object. Fix the bug and related tests.
