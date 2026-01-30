"""Game module containing the main game loop."""


class Game:
    """Main game class that manages the game state and loop."""

    def __init__(self) -> None:
        """Initialize the game."""
        self.running = False

    def run(self) -> None:
        """Start the game loop."""
        self.running = True
        print("Game running...")
