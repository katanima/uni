from raylib import *
import random
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion
from utils import SCREEN_W, SCREEN_H, check_circle_collision


def generate_stars():
    stars = []
    for _ in range(200):
        stars.append([random.uniform(0, SCREEN_W), random.uniform(0, SCREEN_H)])
    return stars


def main():
    InitWindow(SCREEN_W, SCREEN_H, b"Asteroids - Lab 07")
    SetTargetFPS(60)
    InitAudioDevice()

    shoot_sound = LoadSound(b"assets/rocket_blackbox_explode1.wav")
    explode_sound = LoadSound(b"assets/rocket_directhit_explode1.wav")
    death_sound = LoadSound(b"assets/Soldier_paincrticialdeath04.wav")

    stars = generate_stars()

    ship = Ship([SCREEN_W // 2, SCREEN_H // 2])
    ship_respawn_timer = 0.0
    ship_invincible = False

    asteroids = []
    for _ in range(6):
        x = random.uniform(0, SCREEN_W)
        y = random.uniform(0, SCREEN_H)
        radius = random.uniform(15, 40)
        asteroids.append(Asteroid([x, y], radius))

    bullets = []
    explosions = []

    while not WindowShouldClose():
        dt = GetFrameTime()

        if ship_invincible:
            ship_respawn_timer -= dt
            if ship_respawn_timer <= 0:
                ship_invincible = False

        thrust_active = ship.update(dt)

        if IsKeyPressed(KEY_SPACE) and not ship_invincible:
            nose = ship.get_nose_position()
            bullets.append(Bullet(nose, ship.angle))
            PlaySound(shoot_sound)

        for bullet in bullets[:]:
            bullet.update(dt)

        for asteroid in asteroids:
            asteroid.update(dt)

        for explosion in explosions[:]:
            explosion.update(dt)

        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if check_circle_collision(bullet.position, bullet.radius, asteroid.position, asteroid.radius):
                    bullet.alive = False
                    asteroid.alive = False
                    explosions.append(Explosion(asteroid.position, asteroid.radius))
                    PlaySound(explode_sound)

        if not ship_invincible:
            for asteroid in asteroids:
                if check_circle_collision(ship.position, ship.radius, asteroid.position, asteroid.radius):
                    explosions.append(Explosion(ship.position, ship.radius))
                    PlaySound(explode_sound)
                    PlaySound(death_sound)
                    ship = Ship([SCREEN_W // 2, SCREEN_H // 2])
                    ship_invincible = True
                    ship_respawn_timer = 2.0

        bullets = [b for b in bullets if b.alive]
        asteroids = [a for a in asteroids if a.alive]
        explosions = [e for e in explosions if e.alive]

        if len(asteroids) == 0:
            for _ in range(6):
                x = random.uniform(0, SCREEN_W)
                y = random.uniform(0, SCREEN_H)
                radius = random.uniform(15, 40)
                asteroids.append(Asteroid([x, y], radius))

        BeginDrawing()
        ClearBackground(BLACK)

        for star in stars:
            DrawCircle(int(star[0]), int(star[1]), 1, WHITE)

        for bullet in bullets:
            bullet.draw()

        for asteroid in asteroids:
            asteroid.draw()

        for explosion in explosions:
            explosion.draw()

        if ship_invincible:
            if int(GetTime() * 10) % 2 == 0:
                ship.draw()
        else:
            ship.draw()

        if thrust_active and not ship_invincible:
            ship.draw_exhaust()
        ship.draw_debug()

        EndDrawing()

    UnloadSound(shoot_sound)
    UnloadSound(explode_sound)
    CloseAudioDevice()
    CloseWindow()


if __name__ == "__main__":
    main()