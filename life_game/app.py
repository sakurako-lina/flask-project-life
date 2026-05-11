from flask import Flask, render_template
import copy

app = Flask(__name__)

class GameOfLife:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.counter = 0
        self.world = self.create_world()
        self.old_world = copy.deepcopy(self.world)
    
    def create_world(self):
        import random
        world = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(random.choice([0, 1]))
            world.append(row)
        return world
    
    def count_neighbors(self, row, col):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_row = row + i
                neighbor_col = col + j
                if 0 <= neighbor_row < self.height and 0 <= neighbor_col < self.width:
                    count += self.world[neighbor_row][neighbor_col]
        return count
    
    def form_new_generation(self):
        self.old_world = copy.deepcopy(self.world)
        new_world = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                neighbors = self.count_neighbors(i, j)
                cell = self.world[i][j]
                if cell == 1:
                    if neighbors < 2 or neighbors > 3:
                        row.append(0)
                    else:
                        row.append(1)
                else:
                    if neighbors == 3:
                        row.append(1)
                    else:
                        row.append(0)
            new_world.append(row)
        self.world = new_world
    
    def live(self):
        self.counter += 1
        if self.counter > 0:
            self.form_new_generation()
        return self.world

life = GameOfLife(width=20, height=20)

@app.route("/")
def index():
    return render_template("index.html", life=life)

if __name__ == "__main__":
    app.run(debug=True)