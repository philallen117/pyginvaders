"""Test for the player win condition."""

from pyginvaders.config import INVADER_COLS, INVADER_ROWS, KILL_SCORE
from pyginvaders.game import Game


def test_player_won_initialized_to_false():
    """Test that player_won is initialized to False."""
    game = Game()
    assert game.player_won is False


def test_player_wins_when_all_invaders_killed():
    """Test that player_won is set when all invaders are destroyed."""
    game = Game()

    # Record initial number of invaders
    initial_invader_count = len(game.invaders)
    assert initial_invader_count == INVADER_ROWS * INVADER_COLS

    # Simulate killing all invaders except one
    while len(game.invaders) > 1:
        game.invaders.pop()

    assert len(game.invaders) == 1
    assert game.player_won is False

    # Kill the last invader through collision detection
    last_invader = game.invaders[0]
    invader_rect = last_invader.get_rectangle()

    # Fire a bullet at the invader
    bullet = game.player_bullets[0]
    bullet.activate(invader_rect[0], invader_rect[1])

    # Manually trigger collision check
    game.check_player_bullet_collisions()

    # Verify all invaders are gone and player won
    assert len(game.invaders) == 0
    assert game.player_won


def test_player_does_not_win_with_invaders_remaining():
    """Test that player_won remains False when invaders are still alive."""
    game = Game()

    # Kill all but 2 invaders
    while len(game.invaders) > 2:
        game.invaders.pop()

    # Kill one more
    invader = game.invaders[0]
    invader_rect = invader.get_rectangle()

    bullet = game.player_bullets[0]
    bullet.activate(invader_rect[0], invader_rect[1])

    game.check_player_bullet_collisions()

    # Should still have one invader left
    assert len(game.invaders) == 1
    assert game.player_won is False


def test_score_increases_when_winning():
    """Test that score increases appropriately when killing invaders to win."""
    game = Game()

    initial_score = game.score

    # Kill all invaders
    invader_count = len(game.invaders)
    while len(game.invaders) > 0:
        invader = game.invaders[0]
        invader_rect = invader.get_rectangle()

        # Get an inactive bullet
        bullet = None
        for b in game.player_bullets:
            if not b.active:
                bullet = b
                break

        assert bullet is not None, "Should have an available bullet"
        bullet.activate(invader_rect[0], invader_rect[1])
        game.check_player_bullet_collisions()

    # Verify score increased correctly
    expected_score = initial_score + (invader_count * KILL_SCORE)
    assert game.score == expected_score
    assert game.player_won is True


def test_game_state_mutually_exclusive():
    """Test that player_won and game_lost are mutually exclusive."""
    game = Game()

    # Initially both should be False
    assert game.player_won is False
    assert game.game_lost is False

    # Kill all invaders to win
    while len(game.invaders) > 0:
        game.invaders.pop()

    # Trigger a collision check to set player_won
    bullet = game.player_bullets[0]
    bullet.activate(100, 100)
    game.check_player_bullet_collisions()

    # Note: player_won won't be set because no invader was actually hit
    # Let's properly test this
    game2 = Game()

    # Remove all but one invader
    while len(game2.invaders) > 1:
        game2.invaders.pop()

    # Kill the last one
    invader = game2.invaders[0]
    invader_rect = invader.get_rectangle()
    bullet = game2.player_bullets[0]
    bullet.activate(invader_rect[0], invader_rect[1])
    game2.check_player_bullet_collisions()

    # Should be won but not lost
    assert game2.player_won is True
    assert game2.game_lost is False


def test_bullet_deactivates_when_winning_shot():
    """Test that bullet is deactivated when it destroys the last invader."""
    game = Game()

    # Remove all but one invader
    while len(game.invaders) > 1:
        game.invaders.pop()

    invader = game.invaders[0]
    invader_rect = invader.get_rectangle()

    bullet = game.player_bullets[0]
    bullet.activate(invader_rect[0], invader_rect[1])

    assert bullet.active is True

    game.check_player_bullet_collisions()

    assert not bullet.active
    assert game.player_won
