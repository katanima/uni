from raylib import *
import math
from utils import SCREEN_W, SCREEN_H, ghost_positions


class Explosion:
    def __init__(self, position, max_radius):
        self.position = list(position)
        self.max_radius = max_radius
        self.current_radius = 0
        self.alive = True
        self.lifetime = 0.5
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt
        self.current_radius = (self.timer / self.lifetime) * self.max_radius

        if self.timer >= self.lifetime:
            self.alive = False

    def draw(self):
        positions = ghost_positions(self.position[0], self.position[1], self.current_radius)
        for px, py in positions:
            DrawCircleLines(int(px), int(py), int(self.current_radius), ORANGE)