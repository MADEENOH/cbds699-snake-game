import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake Game")

        self.width = 600
        self.height = 400
        self.cell = 20

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#2b2b2b")
        self.canvas.pack()

        self.score = 0
        self.speed = 150
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = 'Right'
        self.running = True
        self.paused = False

        self.label = tk.Label(root, text=f"Score: {self.score}", bg="#2b2b2b", fg="white", font=("Arial", 14))
        self.label.pack()

        self.root.bind("<KeyPress>", self.change_direction)
        self.root.bind("<space>", self.restart_game)
        self.root.bind("<p>", self.toggle_pause)

        self.animate()

    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+self.cell, y+self.cell, fill="#1abc9c", tag="snake", outline="#2b2b2b")

    def create_food(self):
        while True:
            fx = random.randint(0, (self.width - self.cell)//self.cell) * self.cell
            fy = random.randint(0, (self.height - self.cell)//self.cell) * self.cell
            if (fx, fy) not in self.snake:
                return fx, fy

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(x+2, y+2, x+self.cell-2, y+self.cell-2, fill="red", tag="food")

    def move_snake(self):
        x, y = self.snake[0]
        if self.direction == 'Left':
            x -= self.cell
        elif self.direction == 'Right':
            x += self.cell
        elif self.direction == 'Up':
            y -= self.cell
        elif self.direction == 'Down':
            y += self.cell

        new_head = (x, y)

        if x < 0 or x >= self.width or y < 0 or y >= self.height or new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.label.config(text=f"Score: {self.score}")
            self.food = self.create_food()
            self.speed = max(50, self.speed - 2)
        else:
            self.snake.pop()

    def change_direction(self, event):
        key = event.keysym
        opposite = {'Left':'Right', 'Right':'Left', 'Up':'Down', 'Down':'Up'}
        if key in ['Left', 'Right', 'Up', 'Down'] and opposite.get(key) != self.direction:
            self.direction = key

    def animate(self):
        if self.running and not self.paused:
            self.move_snake()
            self.draw_snake()
            self.draw_food()
        self.root.after(self.speed, self.animate)

    def game_over(self):
        self.running = False
        self.canvas.create_text(self.width//2, self.height//2 - 20, text="GAME OVER", fill="white", font=('Arial', 30))
        self.canvas.create_text(self.width//2, self.height//2 + 20, text=f"Final Score: {self.score}", fill="white", font=('Arial', 20))
        self.canvas.create_text(self.width//2, self.height//2 + 60, text="Press SPACE to restart", fill="yellow", font=('Arial', 14))

    def restart_game(self, event):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = 'Right'
        self.score = 0
        self.speed = 150
        self.running = True
        self.paused = False
        self.label.config(text="Score: 0")
        self.canvas.delete("all")

    def toggle_pause(self, event):
        self.paused = not self.paused
        if self.paused:
            self.canvas.create_text(self.width//2, self.height//2, text="PAUSED", fill="yellow", tag="pause", font=("Arial", 25))
        else:
            self.canvas.delete("pause")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
