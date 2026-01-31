To make the code more compact, I want to do some refactorings.

First, make the Game.check_rect_collision method take two 4-tuples of ints - x, y, w, h - corresponding the objects under test, and change call sites of check_rect_collision accordingly.

---

There are several kinds of game play objects to do collision detection for. They will all be rectangles for this purpose. Create a common superclass GameObject with x, y instance variables, an abstract method, in its own module. Add an abstract get_rectangle method class to GameObject. Don't refactor Player, PlayerBullet, Invader, yet.

---

Now refactor Player, PlayerBullet, Invader to use GameObject.
