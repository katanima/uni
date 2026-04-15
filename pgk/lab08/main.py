from raylib import *
import random
import enum
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion
from utils import SCREEN_W, SCREEN_H, check_circle_collision
from config import LEVEL


class GameState(enum.Enum):
    MENU = 1
    GAME = 2
    GAME_OVER = 3


def generate_stars():
    stars = []
    for _ in range(200):
        stars.append([random.uniform(0, SCREEN_W), random.uniform(0, SCREEN_H)])
    return stars


def load_best_score():
    try:
        with open("scores.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def save_best_score(score):
    try:
        with open("scores.txt", "w") as f:
            f.write(str(score))
    except:
        pass


def init_game():
    global ship, asteroids, bullets, explosions, score, wave, wave_delay, wave_timer, ship_invincible, ship_respawn_timer
    ship = Ship([SCREEN_W // 2, SCREEN_H // 2])
    ship_invincible = False
    ship_respawn_timer = 0.0
    asteroids = []
    bullets = []
    explosions = []
    score = 0
    wave = 1
    wave_delay = False
    wave_timer = 0.0

    asteroid_min_size = 15 / (LEVEL * 0.2)
    asteroid_max_size = 40 / (LEVEL * 0.2)

    for _ in range(6):
        x = random.uniform(0, SCREEN_W)
        y = random.uniform(0, SCREEN_H)
        radius = random.uniform(asteroid_min_size, asteroid_max_size)
        asteroids.append(Asteroid([x, y], radius))


def update_menu(dt):
    if IsKeyPressed(KEY_ENTER):
        return GameState.GAME
    return GameState.MENU


def draw_menu():
    ClearBackground(BLACK)
    title = b"LARPING ASTEROIDS"
    start_text = b"PRESS ENTER TO START"
    title_w = MeasureText(title, 40)
    start_w = MeasureText(start_text, 20)
    DrawText(title, SCREEN_W // 2 - title_w // 2, SCREEN_H // 2 - 40, 40, WHITE)
    DrawText(start_text, SCREEN_W // 2 - start_w // 2, SCREEN_H // 2, 20, WHITE)


def update_gameover(dt, victory):
    if IsKeyPressed(KEY_ENTER):
        return GameState.MENU
    return GameState.GAME_OVER


def draw_gameover(victory):
    ClearBackground(BLACK)
    if victory:
        text = b"VICTORY!"
    else:
        text = b"GAME OVER"
    restart = b"PRESS ENTER FOR MENU"
    text_w = MeasureText(text, 40)
    restart_w = MeasureText(restart, 20)
    DrawText(text, SCREEN_W // 2 - text_w // 2, SCREEN_H // 2 - 40, 40, WHITE)
    DrawText(restart, SCREEN_W // 2 - restart_w // 2, SCREEN_H // 2, 20, WHITE)


def update_game(dt):
    global ship, ship_invincible, ship_respawn_timer, asteroids, bullets, explosions, score, best_score, wave, wave_delay, wave_timer, thrust_active

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
                score += asteroid.destroy_score
                if score > best_score:
                    best_score = score
                    save_best_score(best_score)
                asteroids.extend(asteroid.split())
                explosions.append(Explosion(asteroid.position, asteroid.radius))
                PlaySound(explode_sound)

    if not ship_invincible:
        for asteroid in asteroids:
            if check_circle_collision(ship.position, ship.radius, asteroid.position, asteroid.radius):
                explosions.append(Explosion(ship.position, ship.radius))
                PlaySound(explode_sound)
                PlaySound(death_sound)
                return GameState.GAME_OVER, False, thrust_active

    bullets = [b for b in bullets if b.alive]
    asteroids = [a for a in asteroids if a.alive]
    explosions = [e for e in explosions if e.alive]

    if not wave_delay and len(asteroids) == 0:
        wave_delay = True
        wave_timer = 2.0

    if wave_delay:
        wave_timer -= dt
        if wave_timer <= 0:
            wave_delay = False
            wave += 1
            asteroid_min_size = 15 / (LEVEL * 0.2)
            asteroid_max_size = 40 / (LEVEL * 0.2)
            count = 6 + wave
            for _ in range(count):
                x = random.uniform(0, SCREEN_W)
                y = random.uniform(0, SCREEN_H)
                radius = random.uniform(asteroid_min_size, asteroid_max_size)
                asteroids.append(Asteroid([x, y], radius))

    return GameState.GAME, True, thrust_active


def draw_game():
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

    score_text = f"Score: {score}"
    best_text = f"Best: {best_score}"
    wave_text = f"Wave: {wave}"
    DrawText(score_text.encode('utf-8'), 10, 10, 20, WHITE)
    DrawText(best_text.encode('utf-8'), SCREEN_W - 100, 10, 20, WHITE)
    DrawText(wave_text.encode('utf-8'), SCREEN_W // 2 - 30, 10, 20, WHITE)

    if wave_delay:
        next_text = f"WAVE {wave + 1} INCOMING"
        text_w = MeasureText(next_text.encode('utf-8'), 30)
        DrawText(next_text.encode('utf-8'), SCREEN_W // 2 - text_w // 2, SCREEN_H // 2, 30, YELLOW)


def main():
    global stars, shoot_sound, explode_sound, death_sound, thrust_active, score, best_score, wave, wave_delay, wave_timer, ship_invincible, ship_respawn_timer, bullets, asteroids, explosions, ship

    InitWindow(SCREEN_W, SCREEN_H, b"Larping Asteroids")
    SetTargetFPS(60)
    InitAudioDevice()

    shoot_sound = LoadSound(b"assets/rocket_blackbox_explode1.wav")
    explode_sound = LoadSound(b"assets/rocket_directhit_explode1.wav")
    death_sound = LoadSound(b"assets/Soldier_paincrticialdeath04.wav")

    stars = generate_stars()
    thrust_active = False

    state = GameState.MENU
    victory_flag = True
    best_score = load_best_score()

    while not WindowShouldClose():
        dt = GetFrameTime()

        if state == GameState.MENU:
            new_state = update_menu(dt)
            if new_state != state:
                init_game()
                state = new_state
            BeginDrawing()
            draw_menu()
            EndDrawing()

        elif state == GameState.GAME:
            result = update_game(dt)
            if isinstance(result, tuple) and len(result) == 3:
                state, victory_flag, thrust_active = result
            else:
                state = result
                victory_flag = True
            BeginDrawing()
            draw_game()
            EndDrawing()

        elif state == GameState.GAME_OVER:
            new_state = update_gameover(dt, victory_flag)
            if new_state != state:
                state = new_state
            BeginDrawing()
            draw_gameover(victory_flag)
            EndDrawing()

    UnloadSound(shoot_sound)
    UnloadSound(explode_sound)
    UnloadSound(death_sound)
    CloseAudioDevice()
    CloseWindow()


if __name__ == "__main__":
    main()