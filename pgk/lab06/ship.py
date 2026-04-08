from raylib import *
import math
from config import THRUST, HAND_BRAKE, FRICTION, ROTSPEED, MAXSPEED, DEBUG
from utils import ghost_positions, SCREEN_W, SCREEN_H


class Ship:
    def __init__(self, position):
        self.position = list(position)
        self.angle = 0.0
        self.velocity = [0.0, 0.0]
        self.size = 20

        self.vertices = [
            [0, -20],
            [-15, 15],
            [0, 10],
            [15, 15]
        ]

        self.exhaust = [
            [-5, 20],
            [0, 30],
            [5, 20]
        ]

    def rotate_point(self, point, angle):
        x, y = point
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [x * cos_a - y * sin_a, x * sin_a + y * cos_a]

    def wrap(self):
        self.position[0] = self.position[0] % SCREEN_W
        self.position[1] = self.position[1] % SCREEN_H

    def update(self, dt):
        thrust_active = False

        if IsKeyDown(KEY_LEFT):
            self.angle -= ROTSPEED * dt
        if IsKeyDown(KEY_RIGHT):
            self.angle += ROTSPEED * dt

        if IsKeyDown(KEY_UP):
            thrust_active = True
            direction_x = math.sin(self.angle)
            direction_y = -math.cos(self.angle)
            self.velocity[0] += direction_x * THRUST * dt
            self.velocity[1] += direction_y * THRUST * dt

        if IsKeyDown(KEY_Z):
            speed = math.hypot(self.velocity[0], self.velocity[1])

            if speed > 0:
                dir_x = self.velocity[0] / speed
                dir_y = self.velocity[1] / speed

                brake = HAND_BRAKE * dt

                if speed < brake:
                    self.velocity[0] = 0
                    self.velocity[1] = 0
                else:
                    self.velocity[0] -= dir_x * brake
                    self.velocity[1] -= dir_y * brake

        self.velocity[0] *= (1.0 - FRICTION * dt)
        self.velocity[1] *= (1.0 - FRICTION * dt)

        speed = math.hypot(self.velocity[0], self.velocity[1])
        if speed > MAXSPEED:
            self.velocity[0] = self.velocity[0] / speed * MAXSPEED
            self.velocity[1] = self.velocity[1] / speed * MAXSPEED

        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

        self.wrap()

        return thrust_active

    def draw(self):
        positions = ghost_positions(self.position[0], self.position[1], self.size)

        for px, py in positions:
            rotated_vertices = []
            for vertex in self.vertices:
                rotated = self.rotate_point(vertex, self.angle)
                screen_x = px + rotated[0]
                screen_y = py + rotated[1]
                rotated_vertices.append([screen_x, screen_y])

            for i in range(len(rotated_vertices)):
                p1 = rotated_vertices[i]
                p2 = rotated_vertices[(i + 1) % len(rotated_vertices)]
                DrawLine(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), WHITE)

    def draw_exhaust(self):
        positions = ghost_positions(self.position[0], self.position[1], self.size)

        for px, py in positions:
            rotated_exhaust = []
            for vertex in self.exhaust:
                rotated = self.rotate_point(vertex, self.angle)
                screen_x = px + rotated[0]
                screen_y = py + rotated[1]
                rotated_exhaust.append([screen_x, screen_y])

            for i in range(len(rotated_exhaust)):
                p1 = rotated_exhaust[i]
                p2 = rotated_exhaust[(i + 1) % len(rotated_exhaust)]
                DrawLine(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), ORANGE)

    def draw_debug(self):
        if DEBUG:
            speed = math.hypot(self.velocity[0], self.velocity[1])
            if speed > 0:
                end_x = self.position[0] + self.velocity[0] * 0.5
                end_y = self.position[1] + self.velocity[1] * 0.5
                DrawLine(int(self.position[0]), int(self.position[1]),
                         int(end_x), int(end_y), GREEN)

            speed_text = f"Speed: {speed:.1f}"
            vel_text = f"Vel: ({self.velocity[0]:.1f}, {self.velocity[1]:.1f})"
            angle_text = f"Angle: {math.degrees(self.angle):.1f} deg"

            DrawText(speed_text.encode('utf-8'), 10, 10, 20, WHITE)
            DrawText(vel_text.encode('utf-8'), 10, 35, 20, WHITE)
            DrawText(angle_text.encode('utf-8'), 10, 60, 20, WHITE)