Now, we will support the mechanic of player bullets killing invaders and adding to the human player's score.

The `score` is initially zero. The score text displays as described in config. The text is for example "Score: 170".

Add score initialization and display to the game.

---

When a player bullet collides with an invader:

- The invader is removed.
- The bullet returns to the pool and becomes inactive.
- The score increases by KILL_SCORE.

Plan the implementation. There will be other collisions to handle in game logic later on, so I prefer a design where collision logic is easy to reuse.

---

Carry out this plan. Include testing: in each frame,

- Each bullet kills at most one invader
- More than one bullet may strike (different) invaders.
