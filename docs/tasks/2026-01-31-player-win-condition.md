Now, need to implement player win conditions.

First, add game.player_won to game initialization, initially False.

In the game logic, when an invader is killed, check whether there are no longer any invaders left alive.

If none, remain, set player_won to true, and stop updating and drawing objects, analogously to what happens if player_lost.

Plan these changes and unit tests for this logic. We will deal with displaying the won game later.

---

Now, need to implement display of the final score. This analogous to draw_game_lost, with the substitution of the text "You won!" for the text "Game over". For this reason, generalize the current draw_game_lost to be draw_game_over with a parameter message of type string. Then use this generalized method in the game logic for both the game_lost and game_won situations.
