from raylib import *
import math
import random
from utils import ghost_positions, SCREEN_W, SCREEN_H
from config import ASTEROID_BASE_SPEED, ASTEROID_VERTICES, ASTEROID_RADIUS_VARIATION


class Asteroid:
    def __init__(self, position, radius):
        self.position = list(position)
        self.radius = radius
        self.angle = random.uniform(0, math.tau)
        self.rot_speed = random.uniform(-1.5, 1.5)

        speed = ASTEROID_BASE_SPEED * (20.0 / radius) * random.uniform(0.5, 1.5)
        direction = random.uniform(0, math.tau)
        self.velocity = [
            math.cos(direction) * speed,
            math.sin(direction) * speed
        ]

        self.local_vertices = []
        for i in range(ASTEROID_VERTICES):
            vertex_angle = (i / ASTEROID_VERTICES) * math.tau
            r = radius * (1 + random.uniform(-ASTEROID_RADIUS_VARIATION, ASTEROID_RADIUS_VARIATION))
            x = math.cos(vertex_angle) * r
            y = math.sin(vertex_angle) * r
            self.local_vertices.append([x, y])

    def rotate_point(self, point, angle):
        x, y = point
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [x * cos_a - y * sin_a, x * sin_a + y * cos_a]

    def update(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.wrap()
        self.angle += self.rot_speed * dt

    def wrap(self):
        self.position[0] = self.position[0] % SCREEN_W
        self.position[1] = self.position[1] % SCREEN_H

    def draw(self):
        positions = ghost_positions(self.position[0], self.position[1], self.radius)

        for px, py in positions:
            rotated_vertices = []
            for vertex in self.local_vertices:
                rotated = self.rotate_point(vertex, self.angle)
                screen_x = px + rotated[0]
                screen_y = py + rotated[1]
                rotated_vertices.append([screen_x, screen_y])

            for i in range(len(rotated_vertices)):
                p1 = rotated_vertices[i]
                p2 = rotated_vertices[(i + 1) % len(rotated_vertices)]
                DrawLine(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), WHITE)