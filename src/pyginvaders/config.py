"""Game configuration constants."""

import pygame

# Font metrics - calculate actual pixels per point for this system
# This is done at module import time to establish the conversion ratio
pygame.font.init()  # Initialize font system
_TEST_FONT_POINTS = 100  # Use large size for better precision
_test_font = pygame.font.Font(None, _TEST_FONT_POINTS)
_pixel_height = _test_font.get_height()  # Total line height in pixels
PIXELS_PER_POINT: float = _pixel_height / _TEST_FONT_POINTS

# Clean up test variables (keep them private to module)
del _test_font, _pixel_height, _TEST_FONT_POINTS


# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TEXT_COLOR = (255, 255, 255)  # White
SCORE_TEXT_POSITION = (20, 20)
SCORE_TEXT_FONT_POINT_SIZE = int(25 / PIXELS_PER_POINT)  # points
GAME_OVER_TEXT_FONT_POINT_SIZE = int(50 / PIXELS_PER_POINT)  # points

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_SPEED = 5
PLAYER_COLOR = (0, 0, 255)  # Blue

# Player bullet settings
PLAYER_BULLET_WIDTH = 4
PLAYER_BULLET_HEIGHT = 20
PLAYER_BULLET_SPEED = -5  # Negative for upward movement
PLAYER_BULLET_COLOR = (255, 255, 255)  # White
PLAYER_BULLET_POOL_SIZE = 20

# Invader settings
INVADER_WIDTH = 40
INVADER_HEIGHT = 30
INVADER_SPEED_X = 5
INVADER_COLOR = (255, 0, 0)  # Red
INVADER_ROWS = 5
INVADER_COLS = 11
INVADER_START_X = 100
INVADER_START_Y = 50
INVADER_SPACING_X = 60
INVADER_SPACING_Y = 40
INVADER_MOVE_DELAY = 30  # frames
INVADER_DROP_DISTANCE = 20
INVADER_SHOOT_DELAY = 60  # frames
INVADER_SHOOT_CHANCE = 5  # percent chance per delay interval per live invader

KILL_SCORE = 10  # Points per invader killed

# Invader bullet settings
INVADER_BULLET_WIDTH = 4
INVADER_BULLET_HEIGHT = 20
INVADER_BULLET_SPEED = 5
INVADER_BULLET_COLOR = (255, 255, 0)  # Yellow
INVADER_BULLET_POOL_SIZE = 20

# Shield settings
SHIELD_WIDTH = 80
SHIELD_HEIGHT = 60
SHIELD_COLOR = (0, 255, 255)  # Cyan
SHIELD_START_COUNT = 4
SHIELD_START_X = 150
SHIELD_SPACING_X = 150
SHIELD_START_Y = 450
SHIELD_INITIAL_HEALTH = 10  # Number of hits shield can take before being destroyed
SHIELD_ALPHA_REDUCTION = 20  # Alpha reduction per hit (makes shields more visible)
