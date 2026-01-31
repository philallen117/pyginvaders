Now, I want Player to be able to fire bullets.

This task sets up the bullets themselves.

- Player bullets are different from Invader bullets. There is a class called Bullet, already. I want to rename it as PlayerBullet. We will work on invader bullets and factoring out common functionality in a later task.
- There will be a pool of 20 player bullets, which the game will reuse.
- Each player bullet has a boolean field `active` field, which determines whether it is currently in use and displayed. All player bullets are initially inactive.
- Active player bullets display as white rectangles, 4 by 20.
- Active player bullets move upwards at 5 pixels per frame.
- When player bullets reach the top of the screen, they become inactive.

Plan for these changes, and for unit tests that test the logic of movement and becoming inactive at the top of the screen.

---

Add the initialization of the player bullet pool to the Game class.
