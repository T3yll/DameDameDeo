import csv
import tkinter as tk
import matplotlib.pyplot as plt

class Graphic:
    def __init__(self, csv_file):
        self.data = self.read_data_from_csv(csv_file)
        self.avg_positions = self.calculate_average_positions()

        self.plot_scatter()

    def read_data_from_csv(self, csv_file):
        data = {}
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                player = row['Index']
                moves_str = row['game1'] + ',' + row['game2'] + ',' + row['game3']
                moves = [eval(move.strip()) for move in moves_str.split('->')]
                data[player] = moves
        return data

    def calculate_average_positions(self):
        avg_positions = {}
        for player, moves in self.data.items():
            total_x = sum(move[0] for move in moves)
            total_y = sum(move[1] for move in moves)
            avg_x = total_x / len(moves)
            avg_y = total_y / len(moves)
            avg_positions[player] = (avg_x, avg_y)
        return avg_positions

    def plot_scatter(self):
        players = list(self.avg_positions.keys())
        positions = list(self.avg_positions.values())
        colors = ['white' if 'white' in player else 'black' for player in players]

        x, y = zip(*positions)

        plt.figure(figsize=(8, 6))
        plt.scatter(x, y, c=colors, s=100, alpha=0.75)
        plt.xlabel('Position moyenne X')
        plt.ylabel('Position moyenne Y')
        plt.title('Moyenne des positions jouées par joueur')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    def run(self):
        self.root.mainloop()
