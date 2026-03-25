import pyray as rl
import math

# dałem tak bo takie parametry wydawały się być najbardziej optymalne
THRUST = 200.0
HAND_BRAKE = 50.0
FRICTION = 0.98
ROTSPEED = 3.0
MAXSPEED = 400.0
DEBUG = True


class Ship:
    def __init__(self, position, screen_width, screen_height):
        self.position = list(position)
        self.angle = 0.0
        self.velocity = [0.0, 0.0]
        self.screen_width = screen_width
        self.screen_height = screen_height

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

    def update(self, dt):
        thrust_active = False

        if rl.is_key_down(rl.KEY_LEFT):
            self.angle -= ROTSPEED * dt
        if rl.is_key_down(rl.KEY_RIGHT):
            self.angle += ROTSPEED * dt

        if rl.is_key_down(rl.KEY_UP):
            thrust_active = True
            direction_x = math.sin(self.angle)
            direction_y = -math.cos(self.angle)
            self.velocity[0] += direction_x * THRUST * dt
            self.velocity[1] += direction_y * THRUST * dt

        if rl.is_key_down(rl.KEY_Z):
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

        if self.position[0] < 0:
            self.position[0] = 0
            self.velocity[0] = -self.velocity[0]
        if self.position[0] > self.screen_width:
            self.position[0] = self.screen_width
            self.velocity[0] = -self.velocity[0]
        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] = -self.velocity[1]
        if self.position[1] > self.screen_height:
            self.position[1] = self.screen_height
            self.velocity[1] = -self.velocity[1]

        return thrust_active

    def draw(self):
        rotated_vertices = []
        for vertex in self.vertices:
            rotated = self.rotate_point(vertex, self.angle)
            screen_x = self.position[0] + rotated[0]
            screen_y = self.position[1] + rotated[1]
            rotated_vertices.append([screen_x, screen_y])

        for i in range(len(rotated_vertices)):
            p1 = rotated_vertices[i]
            p2 = rotated_vertices[(i + 1) % len(rotated_vertices)]
            rl.draw_line(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), rl.WHITE)

    def draw_exhaust(self):
        rotated_exhaust = []
        for vertex in self.exhaust:
            rotated = self.rotate_point(vertex, self.angle)
            screen_x = self.position[0] + rotated[0]
            screen_y = self.position[1] + rotated[1]
            rotated_exhaust.append([screen_x, screen_y])

        for i in range(len(rotated_exhaust)):
            p1 = rotated_exhaust[i]
            p2 = rotated_exhaust[(i + 1) % len(rotated_exhaust)]
            rl.draw_line(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), rl.ORANGE)

    def draw_debug(self):
        if DEBUG:
            speed = math.hypot(self.velocity[0], self.velocity[1])
            if speed > 0:
                end_x = self.position[0] + self.velocity[0] * 0.5
                end_y = self.position[1] + self.velocity[1] * 0.5
                rl.draw_line(int(self.position[0]), int(self.position[1]),
                             int(end_x), int(end_y), rl.GREEN)

            speed_text = f"Speed: {speed:.1f}"
            vel_text = f"Vel: ({self.velocity[0]:.1f}, {self.velocity[1]:.1f})"
            angle_text = f"Angle: {math.degrees(self.angle):.1f} deg"

            rl.draw_text(speed_text, 10, 10, 20, rl.WHITE)
            rl.draw_text(vel_text, 10, 35, 20, rl.WHITE)
            rl.draw_text(angle_text, 10, 60, 20, rl.WHITE)