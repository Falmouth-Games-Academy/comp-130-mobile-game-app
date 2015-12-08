"""This module includes an enum for representing the directions left, down,
right and up
"""

from kivy.vector import Vector

from enum import Enum

class Direction(Enum):
    """Enum for directions.
    Values are the vectors representing the direction.
    """
    left = Vector(-1, 0)
    down = Vector(0, -1)
    right = Vector(1, 0)
    up = Vector(0, 1)

    def get_angle(self):
        """Return the rotation angle relevant to Direction"""
        if self == Direction.left:
            return 0
        elif self == Direction.down:
            return 90
        elif self == Direction.right:
            return 180
        elif self == Direction.up:
            return 270

    def get_opposite(self):
        """Return the opposite Direction"""
        if self == Direction.left:
            return Direction.right
        elif self == Direction.down:
            return Direction.up
        elif self == Direction.right:
            return Direction.left
        elif self == Direction.up:
            return Direction.down
