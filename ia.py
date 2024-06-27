import random
import pandas as pd
import GameBoard as gb
import generationDico as gd

def evalMoves(gameboard):
    moves_dict = gd.generate_dames_moves()
    all_pieces = gameboard.get_all_pieces_positions()
    black_pieces = []
    for piece in all_pieces:
        if piece["color"] == 1:
            black_pieces.append(piece["position"])
    for piece_position in black_pieces:
        for move in moves_dict:
            #print("Move:", move)
            #print("Piece:", piece_position)
            if move == piece_position:
                moveTest = (move[0] - 1, move[1] + 1)
                print("shakaponk", moveTest)
                for piece in all_pieces:
                    if piece["position"] != moveTest:
                        moves_dict[piece_position] = moves_dict.get(piece_position, 0) + 1

    print(moves_dict)
    max_score = max(moves_dict.values(), default=0)
    best_moves = [move for move, score in moves_dict.items() if score == max_score]
    if not best_moves:
        return None, None
    best_move = random.choice(best_moves)
    print ("Best move:", best_move)
    initial_position = (best_move[0] - 1, best_move[1] + 1)
    print("Best move incremented:", initial_position)
    return best_move , initial_position
    

    # initial_position = None
    # for piece_position, _ in black_pieces:
    #     if best_move in moves_dict.get(piece_position, []):
    #         initial_position = piece_position
    #         break
    # if initial_position is None:
    #     print("No")
    #     return None, None
    # print("Initial:", initial_position)
    # return initial_position, best_move