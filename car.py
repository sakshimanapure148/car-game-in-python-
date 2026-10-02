import tkinter as tk
import random

# Window
root = tk.Tk()
root.title("Car Racing Game")
root.resizable(False, False)

WIDTH = 500
HEIGHT = 600

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="green")
canvas.pack()

# Road
canvas.create_rectangle(100, 0, 400, HEIGHT, fill="gray")

# Road lines
for y in range(0, HEIGHT, 80):
    canvas.create_rectangle(245, y, 255, y + 40, fill="white")

# Player car
car = canvas.create_rectangle(
    220, 500, 280, 570,
    fill="red",
    outline="black",
    width=3
)

# Enemy car
enemy_x = random.randint(120, 340)
enemy = canvas.create_rectangle(
    enemy_x, 50,
    enemy_x + 60, 120,
    fill="blue",
    outline="black",
    width=3
)

score = 0
speed = 5
game_running = True

score_text = canvas.create_text(
    50, 25,
    text="Score: 0",
    font=("Arial", 16, "bold"),
    fill="white"
)


# Move car left
def move_left(event):
    if not game_running:
        return

    x1, y1, x2, y2 = canvas.coords(car)

    if x1 > 105:
        canvas.move(car, -25, 0)


# Move car right
def move_right(event):
    if not game_running:
        return

    x1, y1, x2, y2 = canvas.coords(car)

    if x2 < 395:
        canvas.move(car, 25, 0)


root.bind("<Left>", move_left)
root.bind("<Right>", move_right)


# Move enemy
def move_enemy():
    global score, speed, game_running

    if not game_running:
        return

    canvas.move(enemy, 0, speed)

    enemy_pos = canvas.coords(enemy)
    car_pos = canvas.coords(car)

    # Collision
    if (
        enemy_pos[2] > car_pos[0]
        and enemy_pos[0] < car_pos[2]
        and enemy_pos[3] > car_pos[1]
        and enemy_pos[1] < car_pos[3]
    ):
        game_over()
        return

    # Enemy reached bottom
    if enemy_pos[1] > HEIGHT:

        score += 1
        canvas.itemconfig(
            score_text,
            text="Score: " + str(score)
        )

        # Increase speed
        if score % 5 == 0:
            speed += 1

        # New enemy position
        new_x = random.randint(120, 340)

        canvas.coords(
            enemy,
            new_x, -100,
            new_x + 60, -30
        )

    root.after(30, move_enemy)


# Game over
def game_over():
    global game_running

    game_running = False

    canvas.create_rectangle(
        120, 220, 380, 370,
        fill="white",
        outline="black",
        width=3
    )

    canvas.create_text(
        250, 260,
        text="GAME OVER",
        font=("Arial", 30, "bold"),
        fill="red"
    )

    canvas.create_text(
        250, 310,
        text="Score: " + str(score),
        font=("Arial", 20, "bold"),
        fill="black"
    )

    canvas.create_text(
        250, 345,
        text="Press R to Restart",
        font=("Arial", 14),
        fill="black"
    )


# Restart
def restart(event):
    global score, speed, game_running

    if game_running:
        return

    score = 0
    speed = 5
    game_running = True

    canvas.delete("all")

    # Road
    canvas.create_rectangle(
        100, 0, 400, HEIGHT,
        fill="gray"
    )

    # Road lines
    for y in range(0, HEIGHT, 80):
        canvas.create_rectangle(
            245, y, 255, y + 40,
            fill="white"
        )

    # Player car
    global car, enemy, score_text

    car = canvas.create_rectangle(
        220, 500, 280, 570,
        fill="red",
        outline="black",
        width=3
    )

    # Enemy
    enemy_x = random.randint(120, 340)

    enemy = canvas.create_rectangle(
        enemy_x, 50,
        enemy_x + 60, 120,
        fill="blue",
        outline="black",
        width=3
    )

    score_text = canvas.create_text(
        50, 25,
        text="Score: 0",
        font=("Arial", 16, "bold"),
        fill="white"
    )

    move_enemy()


root.bind("<r>", restart)
root.bind("<R>", restart)

# Start
move_enemy()

root.mainloop()