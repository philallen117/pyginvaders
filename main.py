"""Main entry point for PyGInvaders."""

from pyginvaders.game import Game


def main() -> None:
    """Run the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
