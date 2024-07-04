import random
import pandas as pd
import GameBoard as gb
import generationDico as gd
import numpy as np
import os




def compareColListe(df:pd.DataFrame, liste):
    return np.isin(liste,df).all()

def evalMoves(gb:gb.GameBoard):
    moves_dict,dicoEat = gd.generate_dames_moves(gb)
    currstr=random.choice(list(moves_dict.keys()))
    current=currstr
    best_move= moves_dict[current][0]
    mange=None
    poids={10:[],5:[],0:[]}
    method="random"

    if os.path.exists('moves1.csv'):
        csv= pd.read_csv('moves1.csv')
    else:
        csv = pd.DataFrame()
    for i in csv.columns[1:]:
        if compareColListe(csv[i],gb.allMoves): # si la sequence actuelle de jeu se trouve dans le csv
            if len(gb.allMoves)==0:
                print(csv[csv.columns[0]][0])
                if csv[csv.columns[0]][0].startswith("black"):
                    tmp = csv[i][0]
                    print("vide")
                    poids[10].append(csv[i][0])
                else:
                    tmp = csv[i][1]
                    if pd.notna(tmp):
                        poids[10].append(tmp)
                    print("pas vide")
            else:
                tmp = gb.allMoves[gb.game.tour-1]
                poids[10].append(tmp)
            print("tmp ",tmp)

            poids = {k: v for k, v in poids.items() if len(v)>0}
            print(poids)
            tmp= random.choice(poids[max(poids.keys())])

            tmp = tmp.replace(" -> ", ",")
            tmp= eval("["+tmp+"]")
            best_move=tmp[1]
            currstr=str(tmp[0])
            method="chosen"
        else:
            if len(dicoEat)>0:
                currstr=random.choice(list(dicoEat.keys()))
                current=eval(currstr)
                
                print("mange IA")
                mange=dicoEat[currstr][random.randint(0,len(dicoEat[currstr])-1)]
                depart = gb.getParcourIA(current,mange)
                best_move = eval(currstr)
                currstr = str(depart)

            else:
                currstr = random.choice(list(moves_dict.keys()))
                current=eval(currstr)
                #print("bouge IA")
                
                best_move = moves_dict[currstr][random.randint(0,len(moves_dict[currstr])-1)]
            method="random"

    if mange!=None:
        gb.game.grid[mange[0]][mange[1]]=0
    print("best move " + method + " : ", currstr, "->", best_move)
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