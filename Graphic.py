import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

class Graphic:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file, header=None)
        self.columns = ['Player'] + [f'Game{i}' for i in range(1, len(self.data.columns))]
        self.data.columns = self.columns
        self.white_positions = []
        self.black_positions = []
        self.avg_white_position = (None, None)
        self.avg_black_position = (None, None)
        self._extract_positions()

    def _extract_positions(self):
        def extract_positions(move):
            positions = re.findall(r'\[(\d+), (\d+)\]', move)
            return [(int(x), int(y)) for x, y in positions]

        for index, row in self.data.iterrows():
            player = row['Player']
            moves = row[1:].dropna()
            
            for move in moves:
                positions = extract_positions(move)
                if player.startswith('white'):
                    self.white_positions.extend(positions)
                elif player.startswith('black'):
                    self.black_positions.extend(positions)
                    
        self.avg_white_position = self._average_position(self.white_positions)
        self.avg_black_position = self._average_position(self.black_positions)

    def _average_position(self, positions):
        if positions:
            x, y = zip(*positions)
            return np.mean(x), np.mean(y)
        return None, None

    def plot_positions(self):
        white_x, white_y = zip(*self.white_positions)
        black_x, black_y = zip(*self.black_positions)

        plt.figure(figsize=(10, 10))
        plt.scatter(white_x, white_y, color='blue', label='White Positions')
        plt.scatter(black_x, black_y, color='red', label='Black Positions')
        plt.scatter(*self.avg_white_position, color='blue', marker='x', s=100, label='Average White Position')
        plt.scatter(*self.avg_black_position, color='red', marker='x', s=100, label='Average Black Position')

        plt.title('Positions of White and Black Pieces')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.legend()
        plt.grid(True)
        plt.show()

