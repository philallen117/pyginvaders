"""Tests for shield and invader bullet collision interactions."""

from pyginvaders.config import SHIELD_INITIAL_HEALTH
from pyginvaders.game import Game


def test_invader_bullet_hits_shield():
    """Test that invader bullet hitting shield deactivates bullet."""
    game = Game()

    shield = game.shields[0]
    shield_rect = shield.get_rectangle()

    # Activate bullet directly above shield
    bullet = game.invader_bullets[0]
    bullet.activate(shield_rect[0] + 10, shield_rect[1] - 10)

    assert bullet.active is True

    # Move bullet into shield
    bullet.update()

    # Check collision
    game.check_invader_bullet_shield_collisions()

    # Bullet should be deactivated
    assert not bullet.active


def test_shield_takes_damage_on_hit():
    """Test that shield health decreases when hit by invader bullet."""
    game = Game()

    shield = game.shields[0]
    initial_health = shield.health
    shield_rect = shield.get_rectangle()

    # Position bullet to hit shield
    bullet = game.invader_bullets[0]
    bullet.activate(shield_rect[0] + 10, shield_rect[1] + 5)

    # Check collision
    game.check_invader_bullet_shield_collisions()

    # Shield health should be reduced
    assert shield.health == initial_health - 1


def test_shield_destroyed_when_health_zero():
    """Test that shield is removed when health reaches 0."""
    game = Game()

    shield = game.shields[0]
    initial_shield_count = len(game.shields)

    # Damage shield to zero health
    for _ in range(SHIELD_INITIAL_HEALTH):
        shield.take_damage()

    # Verify shield is destroyed
    assert shield.is_destroyed() is True

    # Activate bullet to hit destroyed shield
    shield_rect = shield.get_rectangle()
    bullet = game.invader_bullets[0]
    bullet.activate(shield_rect[0] + 10, shield_rect[1] + 5)

    # Check collision (should remove shield from list)
    game.check_invader_bullet_shield_collisions()

    # Shield should be removed from game
    assert len(game.shields) == initial_shield_count - 1
    assert shield not in game.shields


def test_bullet_hits_only_one_shield():
    """Test that a bullet can only hit one shield per frame."""
    game = Game()

    # Position first shield
    shield1 = game.shields[0]
    shield1_rect = shield1.get_rectangle()

    # Position second shield nearby
    shield2 = game.shields[1]

    # Activate bullet between them (closer to shield1)
    bullet = game.invader_bullets[0]
    bullet.activate(shield1_rect[0] + 10, shield1_rect[1] + 5)

    # Check collision
    game.check_invader_bullet_shield_collisions()

    # Only one shield should be damaged
    damaged_shields = sum(
        [
            1
            for s in [shield1, shield2]
            if s in game.shields and s.health < SHIELD_INITIAL_HEALTH
        ]
    )
    assert damaged_shields == 1


def test_multiple_bullets_can_damage_shield():
    """Test that multiple bullets can each damage a shield."""
    game = Game()

    shield = game.shields[0]
    shield_rect = shield.get_rectangle()
    initial_health = shield.health

    # Fire 3 bullets at the shield
    for i in range(3):
        bullet = game.invader_bullets[i]
        bullet.activate(shield_rect[0] + 10, shield_rect[1] + 5)
        game.check_invader_bullet_shield_collisions()

    # Shield should have taken 3 damage
    assert shield.health == initial_health - 3


def test_shield_protects_player():
    """Test that shield blocks bullet from reaching player."""
    game = Game()

    shield = game.shields[0]
    shield_rect = shield.get_rectangle()

    # Position bullet above shield
    bullet = game.invader_bullets[0]
    bullet.activate(shield_rect[0] + 10, shield_rect[1] - 10)

    # Update bullet (moves down into shield)
    bullet.update()

    # Check shield collision first
    game.check_invader_bullet_shield_collisions()

    # Bullet should be inactive after hitting shield
    assert bullet.active is False

    # Now check player collision - bullet is already inactive
    hit_player = game.check_invader_bullet_collisions()

    # Player should not be hit
    assert hit_player is False


def test_destroyed_shields_dont_block_bullets():
    """Test that destroyed shields are removed and don't block bullets."""
    game = Game()

    shield = game.shields[0]
    shield_rect = shield.get_rectangle()

    # Destroy the shield
    for _ in range(SHIELD_INITIAL_HEALTH):
        shield.take_damage()

    # Remove shield manually (simulating previous collision)
    if shield.is_destroyed() and shield in game.shields:
        game.shields.remove(shield)

    # Fire bullet where shield used to be
    bullet = game.invader_bullets[0]
    bullet.activate(shield_rect[0] + 10, shield_rect[1] + 5)

    # Check collision
    game.check_invader_bullet_shield_collisions()

    # Bullet should still be active (no shield to hit)
    assert bullet.active is True


def test_reset_game_creates_shields_with_full_health():
    """Test that reset_game creates shields with full health."""
    game = Game()

    # Damage first shield
    game.shields[0].take_damage()
    game.shields[0].take_damage()

    # Reset game
    game.reset_game()

    # All shields should have full health
    for shield in game.shields:
        assert shield.health == SHIELD_INITIAL_HEALTH
