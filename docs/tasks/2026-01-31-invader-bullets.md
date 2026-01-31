Time to build invader bullets. First, we will deal with their basic set-up. Shooting and collision will come later.

- InvaderBullet should be a subclass of GameObject.
- It's dimensions, color and speed (downwards) are described in src/pyginvaders/config.py
- Similarly to PlayerBullet, we will use a pool of INVADER_BULLET_POOL_SIZE. InvaderBullets. InvaderBullet has an `active` instance variable initially `false`.
- InvaderBullets move down the screen.

Implement the class with movement and drawing, and implement the pool in Game. Implement unit tests for movement and pool creation.

---- BREAK for commit.
