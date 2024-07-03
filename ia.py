import random
import pandas as pd
import GameBoard as gb
import generationDico as gd
import numpy as np
import os




def compareColListe(df:pd.DataFrame, liste):
    return np.isin(df, liste).all()

def evalMoves(gb:gb.GameBoard):
    moves_dict,dicoEat = gd.generate_dames_moves(gb)
    currstr=random.choice(list(moves_dict.keys()))
    current=currstr
    best_move= moves_dict[current][0]
    mange=None


    if os.path.exists('moves1.csv'):
        csv= pd.read_csv('moves1.csv')
    else:
        csv = pd.DataFrame()
    for i in csv.columns[1:]:
        if compareColListe(csv[i],gb.allMoves): # si la sequence actuelle de jeu se trouve dans le csv
            tmp = gb.allMoves[gb.game.tour-1]
            tmp.replace(" -> ", ",")
            tmp= eval("["+tmp+"]")
            best_move=tmp[1]
            current=tmp[0]
            method="chosen"
        else:
            if len(dicoEat)>0:
                currstr=random.choice(list(dicoEat.keys()))
                current=eval(currstr)
                
                print("mange IA")
                mange=dicoEat[currstr][random.randint(0,len(dicoEat[currstr])-1)]
                arrivee = gb.getParcourIA(current,mange)
                best_move =  arrivee
            else:
                current=random.choice(list(moves_dict.keys()))
                #print("bouge IA")
                
                best_move = moves_dict[current][random.randint(0,len(moves_dict[current])-1)]
            method="random"
    print("best move " +method+ " : ",current,"->", best_move)  
    if mange!=None:
        gb.game.grid[mange[0]][mange[1]]=0
    return best_move, currstr

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