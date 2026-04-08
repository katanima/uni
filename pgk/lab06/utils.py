SCREEN_W = 800
SCREEN_H = 600


def ghost_positions(x, y, size):
    positions = [(x, y)]

    if x - size < 0:
        positions.append((x + SCREEN_W, y))
    if x + size > SCREEN_W:
        positions.append((x - SCREEN_W, y))

    if y - size < 0:
        new_positions = []
        for px, py in positions:
            if (px, py) != (x, y) or len(positions) == 1:
                new_positions.append((px, py + SCREEN_H))
        positions.extend(new_positions)
    if y + size > SCREEN_H:
        new_positions = []
        for px, py in positions:
            if (px, py) != (x, y) or len(positions) == 1:
                new_positions.append((px, py - SCREEN_H))
        positions.extend(new_positions)

    return positions