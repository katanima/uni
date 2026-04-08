from raylib import *
import random
from ship import Ship
from asteroid import Asteroid
from utils import SCREEN_W, SCREEN_H


def main():
    InitWindow(SCREEN_W, SCREEN_H, b"Asteroids - Lab 06")
    SetTargetFPS(60)

    ship = Ship([SCREEN_W // 2, SCREEN_H // 2])

    asteroids = []
    for _ in range(6):
        x = random.uniform(0, SCREEN_W)
        y = random.uniform(0, SCREEN_H)
        radius = random.uniform(15, 40)
        asteroids.append(Asteroid([x, y], radius))

    while not WindowShouldClose():
        dt = GetFrameTime()

        thrust_active = ship.update(dt)

        for asteroid in asteroids:
            asteroid.update(dt)

        BeginDrawing()
        ClearBackground(BLACK)

        ship.draw()
        if thrust_active:
            ship.draw_exhaust()
        ship.draw_debug()

        for asteroid in asteroids:
            asteroid.draw()

        EndDrawing()

    CloseWindow()


if __name__ == "__main__":
    main()