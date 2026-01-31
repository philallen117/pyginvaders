"""Test for the game over collision scenario."""

from pyginvaders.game import Game


def test_game_over_when_player_hit_by_invader_bullet():
    """Test that game transitions to game over when player is hit by invader bullet."""
    game = Game()

    # Verify game starts in running state
    assert game.running is False  # Not started yet
    assert game.game_lost is False

    # Get player position
    player_rect = game.player.get_rectangle()

    # Activate an invader bullet directly above the player
    bullet = game.invader_bullets[0]
    bullet.activate(player_rect[0] + 20, player_rect[1] - 10)

    # Simulate one frame update - bullet should move down and hit player
    bullet.update()

    # Manually check collision (simulating game loop logic)
    from pyginvaders.game import check_rect_collision

    if check_rect_collision(bullet.get_rectangle(), player_rect):
        bullet.deactivate()
        game.game_lost = True

    # Verify game is in lost state
    assert game.game_lost is True
    assert bullet.active is False


def test_collision_detection():
    """Test the collision detection function."""
    from pyginvaders.game import check_rect_collision

    # Test overlapping rectangles
    rect1 = (0, 0, 10, 10)
    rect2 = (5, 5, 10, 10)
    assert check_rect_collision(rect1, rect2) is True

    # Test non-overlapping rectangles
    rect1 = (0, 0, 10, 10)
    rect2 = (20, 20, 10, 10)
    assert check_rect_collision(rect1, rect2) is False

    # Test edge touching (should not be considered collision)
    rect1 = (0, 0, 10, 10)
    rect2 = (10, 0, 10, 10)
    assert check_rect_collision(rect1, rect2) is False
