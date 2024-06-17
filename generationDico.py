def generate_dames_moves():
    dames_moves = {}
    for row in range(10):
        for col in range(10):
            if (row + col) % 2 != 0:
                coord = (row, col)
                dames_moves[coord] = 0
    return dames_moves