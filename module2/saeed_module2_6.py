# 2048 Game Implementation in Python
# This code creates a simple console-based version of the 2048 game.
# Players can move tiles using 'w', 'a', 's', 'd' keys to slide tiles up, left, down, and right respectively.
# The game ends when the player reaches the 2048 tile or when no moves are possible.
# Rafrance https://en.wikipedia.org/wiki/2048_(video_game)
import random
import os
import sys

class Game2048:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def display(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("Score:", self.score)
        print("+----+----+----+----+")
        for row in self.grid:
            print("|", end="")
            for cell in row:
                if cell == 0:
                    print("    |", end="")
                else:
                    print(f"{cell:4}|", end="")
            print()
            print("+----+----+----+----+")

    def move(self, direction):
        moved = False
        if direction == 'up':
            for j in range(4):
                col = [self.grid[i][j] for i in range(4)]
                new_col = self.slide_and_merge(col)
                for i in range(4):
                    if self.grid[i][j] != new_col[i]:
                        moved = True
                    self.grid[i][j] = new_col[i]
        elif direction == 'down':
            for j in range(4):
                col = [self.grid[i][j] for i in range(3, -1, -1)]
                new_col = self.slide_and_merge(col)
                for i in range(3, -1, -1):
                    if self.grid[i][j] != new_col[3-i]:
                        moved = True
                    self.grid[i][j] = new_col[3-i]
        elif direction == 'left':
            for i in range(4):
                row = self.grid[i]
                new_row = self.slide_and_merge(row)
                if self.grid[i] != new_row:
                    moved = True
                self.grid[i] = new_row
        elif direction == 'right':
            for i in range(4):
                row = self.grid[i][::-1]
                new_row = self.slide_and_merge(row)[::-1]
                if self.grid[i] != new_row:
                    moved = True
                self.grid[i] = new_row
        if moved:
            self.add_new_tile()

    def slide_and_merge(self, line):
        # Remove zeros
        line = [x for x in line if x != 0]
        # Merge
        for i in range(len(line) - 1):
            if line[i] == line[i+1]:
                line[i] *= 2
                self.score += line[i]
                line[i+1] = 0
        # Remove zeros again
        line = [x for x in line if x != 0]
        # Pad with zeros
        line += [0] * (4 - len(line))
        return line

    def is_win(self):
        return any(2048 in row for row in self.grid)

    def is_lose(self):
        if any(0 in row for row in self.grid):
            return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.grid[i][j] == self.grid[i+1][j]) or (j < 3 and self.grid[i][j] == self.grid[i][j+1]):
                    return False
        return True

def main():
    game = Game2048()
    while True:
        game.display()
        if game.is_win():
            print("You win!")
            break
        if game.is_lose():
            print("You lose!")
            break
        move = input("Move (w/a/s/d): ").lower()
        if move in ['w', 'a', 's', 'd']:
            direction = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}[move]
            game.move(direction)
        else:
            print("Invalid move")