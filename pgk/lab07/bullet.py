from raylib import *
import math
from utils import ghost_positions, SCREEN_W, SCREEN_H
from config import BULLET_SPEED, BULLET_TTL, BULLET_RADIUS


class Bullet:
    def __init__(self, position, angle):
        self.position = list(position)
        self.radius = BULLET_RADIUS
        self.alive = True
        self.ttl = BULLET_TTL

        direction_x = math.sin(angle)
        direction_y = -math.cos(angle)
        self.velocity = [
            direction_x * BULLET_SPEED,
            direction_y * BULLET_SPEED
        ]

    def update(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.wrap()

        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False

    def wrap(self):
        self.position[0] = self.position[0] % SCREEN_W
        self.position[1] = self.position[1] % SCREEN_H

    def draw(self):
        positions = ghost_positions(self.position[0], self.position[1], self.radius)
        for px, py in positions:
            DrawCircle(int(px), int(py), self.radius, WHITE)