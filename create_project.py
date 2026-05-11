import os

os.makedirs('life_game/templates', exist_ok=True)
os.makedirs('life_game/static', exist_ok=True)


app_py_content = '''from flask import Flask, render_template
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
'''

# 2. Создаём index.html
index_html_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Игра "Жизнь"</title>
    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'style.css\') }}">
    <meta http-equiv="refresh" content="2">
</head>
<body>
    <h1>Игра "Жизнь" Конвея</h1>
    
    <!-- Счётчик поколений -->
    <div class="counter">{{ life.counter }}</div>
    
    <!-- Игровое поле -->
    <table class="world">
        {% for i in range(life.height) %}
        <tr>
            {% for j in range(life.width) %}
            {% if life.world[i][j] %}
                <td class="cell living-cell"></td>
            {% elif life.world[i][j] == 0 and life.old_world[i][j] == 1 %}
                <td class="cell dead-cell"></td>
            {% else %}
                <td class="cell"></td>
            {% endif %}
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    
    <p>Страница обновляется автоматически каждые 2 секунды</p>
</body>
</html>
'''

# 3. Создаём style.css
style_css_content = '''body {
    font-family: Arial, sans-serif;
    text-align: center;
    background-color: #f0f0f0;
    padding: 20px;
}

h1 {
    color: #333;
}

.counter {
    font-size: 24px;
    font-weight: bold;
    color: #0066cc;
    margin: 20px 0;
    padding: 10px 20px;
    background-color: #fff;
    border-radius: 5px;
    display: inline-block;
}

.world {
    border-collapse: collapse;
    margin: 20px auto;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.cell {
    width: 25px;
    height: 25px;
    border: 1px solid #ddd;
    background-color: #ffffff;
}

.living-cell {
    background-color: #4CAF50;
    border: 1px solid #45a049;
}

.dead-cell {
    background-color: #f44336;
    border: 1px solid #da190b;
}

p {
    color: #666;
    margin-top: 20px;
}
'''

# 4. Создаём requirements.txt
requirements_txt_content = '''Flask>=2.0.0
'''

# 5. Создаём .gitignore
gitignore_content = '''__pycache__/
*.pyc
*.pyo
.env
venv/
.venv/
*.db
.DS_Store
'''

# Записываем все файлы
with open('life_game/app.py', 'w', encoding='utf-8') as f:
    f.write(app_py_content)

with open('life_game/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html_content)

with open('life_game/static/style.css', 'w', encoding='utf-8') as f:
    f.write(style_css_content)

with open('life_game/requirements.txt', 'w', encoding='utf-8') as f:
    f.write(requirements_txt_content)

with open('life_game/.gitignore', 'w', encoding='utf-8') as f:
    f.write(gitignore_content)

print("✅ Проект 'life_game' успешно создан!")
print("\\nСтруктура проекта:")
print("life_game/")
print("├── app.py")
print("├── requirements.txt")
print("├── .gitignore")
print("├── templates/")
print("│   └── index.html")
print("└── static/")
print("    └── style.css")
print("\\n📋 Следующие шаги:")
print("1. cd life_game")
print("2. pip install -r requirements.txt")
print("3. python app.py")
print("4. Откройте http://127.0.0.1:5000/")