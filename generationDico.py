import pandas as pd


'''
def generate_dames_moves():
    
    moves_dict = {}
    def is_within_board(x, y):
        return 0 <= x < 10 and 0 <= y < 10
    for row in range(10):
        for col in range(10):
            if (row + col) % 2 == 0:  #cases noires
                coord = (row, col)
                directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if is_within_board(new_row, new_col):
                        new_coord = (new_row, new_col)
                        moves_dict[new_coord] = 0
    moves_df = pd.DataFrame(moves_dict.items(), columns=['Coordonnee', 'Valeur'])
    moves_df.to_csv('moves.csv', index=False)
    return moves_dict
    
'''


def is_within_board(x, y):
    return 0 <= x < 10 and 0 <= y < 10


def generate_dames_moves(grid):
    moves_dict = {}

