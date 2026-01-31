I want to factor out game configuration constants that are used in several places, so as not to have to pass them around as method parameters.

Start with screen height and width.

What Pythonic design do you recommend?

---

Implement a simple config module.

---

The player constants are copied into instance variables in the Player class. But they will never change. Please remove the width, height, color and speed instance variables and refer directly to PLAYER_WIDTH etc. directly instead.
