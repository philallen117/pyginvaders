Time to build invader bullets. First, we will deal with their basic set-up. Shooting and collision will come later.

- InvaderBullet should be a subclass of GameObject.
- It's dimensions, color and speed (downwards) are described in src/pyginvaders/config.py
- Similarly to PlayerBullet, we will use a pool of INVADER_BULLET_POOL_SIZE. InvaderBullets. InvaderBullet has an `active` instance variable initially `false`.
- InvaderBullets move down the screen.

Implement the class with movement and drawing, and implement the pool in Game. Implement unit tests for movement and pool creation.

---- BREAK for commit.

Factor out a common Bullet superclass from PlayerBullet and InvaderBullet promoting common methods, and making other methods (e.g. update) abstract.
On grounds of simplicity, i would like to keep draw() abstract on Bullet. Show me the updated plan.
First, show me a plan.

--- BREAK for commit.

Now add player bullet collision logic.

First, add an instance variable called game_lost to game, initially false.

If an invader bullet collides with the Player object, the game is lost. I prefer the update of dead invaders and score to be done before the update of game_lost. Update the game logic and tests accordingly. We will deal with displaying the final outcome later.

---

Quick tidy-up. In the game logic around line 146, the should use get_rectangle on the invader and the player bullet. Moreover, for efficiency, the code should get the bullet rectangle in the bullet loop before the invader loop is entered. Make the change.

--- BREAK for commit

Now, we need invaders to fire bullets.

At intervals on INVADER_SHOOT_DELAY, all invaders randomly decide shoot, each with probability INVADER_SHOOT_CHANCE per cent.

If an invader decides to shoot, the game takes an inactive bullet from the pool and makes it active. (If no bullets are inactive, nothing further happens this frame; this is not an error.) As you can see, this part is analogous to player bullets.

When an invader shoots, the bullet appears at the bottom centre of that invader.

Note that invader bullets pass over other invaders without interacting with them.

Plan the change and unit tests for it.

---

That is good, but while doing that please factor out a method fire_invader_bullet, analogously to fire_bullet (which fires player bullet)
