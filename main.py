import tkinter as tk
import random
import time 
import json
import pygame

with open('scores.json', 'r') as file:
    data = json.load(file)

direction_of_snake = "w"
snake_body = []
score = 0
high_score = data["high_score"]
high_score_player = data["player"]
player = ""


def get_input_and_continue():
    global player
    player = entry.get()
    
    entry.destroy()
    submit_button.destroy()
    root0.destroy()

root0 = tk.Tk()
root0.title("Input Example")

entry = tk.Entry(root0, width=30)
entry.pack(pady=10)

submit_button = tk.Button(root0, text="Submit", command=get_input_and_continue)
submit_button.pack(pady=10)

root0.mainloop()


root = tk.Tk()
root.title("Snake Game Board")

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1) 

high_score_label = tk.Label(text="The high score is: "+ str(data["high_score"])+"  - "+data["player"])
high_score_label.pack()
board_size = 9

board_labels = [[None for _ in range(board_size)] for _ in range(board_size)]

board_frame = tk.Frame(root, bg="gray")
board_frame.pack(padx=10, pady=10)

score_label = tk.Label(root, text="Score: 0", font=("Arial", 16))
score_label.pack(pady=5)

for row in range(board_size):
    for col in range(board_size):
        label = tk.Label(
            board_frame,
            width=4,
            height=2,
            bg="white",
            relief="solid",
            borderwidth=0,
            fg="#8a8a8a",
            padx=0,
            pady=0
        )
        label.grid(row=row, column=col, padx=1, pady=1)
        board_labels[col][row] = label


def play_again():
    global high_score
    for row in range(board_size):
        for col in range(board_size):
            board_labels[col][row].config(bg="#ffffff")
    button.destroy()
    if score > high_score:
        high_score = score
        data["high_score"] = high_score
        data["player"] = player
        high_score_label.config(text="The high score is: "+ str(data["high_score"])+"  - "+data["player"])
        with open('scores.json', 'w') as file:
            json.dump(data, file, indent=4)
    start_game()

def game_on():
    global snake_head_x, snake_head_y, food_square_x, food_square_y, snake_tail_x, snake_tail_y, score, score_label, button
    while True:
        if direction_of_snake == "w":
            snake_head_y = snake_head_y - 1
        elif direction_of_snake == "s":
            snake_head_y = snake_head_y + 1
        elif direction_of_snake == "a":
            snake_head_x = snake_head_x - 1
        elif direction_of_snake == "d":
            snake_head_x = snake_head_x + 1

        body_part = str(snake_head_x) + str(snake_head_y)

        if snake_head_x not in range(0, board_size) or snake_head_y not in range(0, board_size):
            score_label.configure(text="You lost, your score is: " + str(score) + " Click the button if you want to play again")
            score_label.update()
            break
        elif body_part in snake_body:
            score_label.configure(text="You lost, your score is: " + str(score) + " Click the button if you want to play again")
            score_label.update()
            break
   
        board_labels[snake_head_x][snake_head_y].configure(bg="#000000")
        snake_body.insert(0, body_part)

        if snake_head_x == food_square_x and snake_head_y == food_square_y:
            while str(food_square_x)+str(food_square_y) in snake_body:
                food_square_x = random.randint(0,board_size-1)
                food_square_y = random.randint(0,board_size-1)
            board_labels[food_square_x][food_square_y].configure(bg="#ff0000") 
            score = score + 1
            score_label.configure(text="Score: " + str(score))
            score_label.update()
        else:
            board_labels[snake_head_x][snake_head_y].configure(bg="#000000")
            board_labels[snake_head_x][snake_head_y].update()
            time.sleep(0.1)

            board_labels[snake_tail_x][snake_tail_y].configure(bg="#ffffff")
            board_labels[snake_tail_x][snake_tail_y].update()
            snake_body.pop()
            snake_tail_x = int(snake_body[-1][0])
            snake_tail_y = int(snake_body[-1][1])

            

        root.update()
        time.sleep(0.1)
    button = tk.Button(root, text="Play again", command=play_again)
    button.pack(pady=5)

def start_game():
    global snake_head_x, snake_head_y, food_square_x, food_square_y, snake_tail_x, snake_tail_y, score, snake_body, direction_of_snake
    score = 0
    snake_body = []
    direction_of_snake = "w"
    snake_head_x = 4
    snake_head_y = 6
    snake_tail_x = snake_head_x
    snake_tail_y = snake_head_y
    body_part = str(snake_head_x) + str(snake_head_y)
    snake_body.append(body_part)
    score_label.configure(text="Score: "+ str(score))
    score_label.update()

    board_labels[snake_head_x][snake_head_y].configure(bg="#000000")

    food_square_x = snake_head_x
    food_square_y = snake_head_y

    while food_square_x == snake_head_x and food_square_y == snake_head_y:
        food_square_x = random.randint(0,board_size-1)
        food_square_y = random.randint(0,board_size-1)
    board_labels[food_square_x][food_square_y].configure(bg="#ff0000")
    game_on()


def on_key_press(event):
    global direction_of_snake
    if event.char == "w": 
        direction_of_snake = "w"
    elif event.char == "a": 
        direction_of_snake = "a"
    elif event.char == "s": 
        direction_of_snake = "s"
    elif event.char == "d": 
        direction_of_snake = "d"

root.bind("<KeyPress>", on_key_press)
start_game()

root.mainloop()
