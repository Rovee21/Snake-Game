from tkinter import *
import random

GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 50
BODY_PEICES = 2
SNAKE_COLOR = "ORANGE"
FOOD_COLOR = "RED"
BG_COLOR = "BLACK"

class Snake:
    
    def __init__(self):
        self.body_size = BODY_PEICES
        self.coordinates = []
        self.squares = []

        for i in range(0,BODY_PEICES):
            self.coordinates.append([0,0])

        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y,x+SPACE_SIZE, y+SPACE_SIZE, fill= SNAKE_COLOR, tag = "snake")
            self.squares.append(square)
class Food:
    
    def __init__(self):
        x = random.randint(0,(GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0,(GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x,y]

        canvas.create_oval(x,y,x+SPACE_SIZE, y+SPACE_SIZE, fill = FOOD_COLOR, tag = "food")


def nextTurn(snake, food):
    
    x,y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0,(x,y))

    square = canvas.create_rectangle(x,y,x+SPACE_SIZE, y+SPACE_SIZE, fill= SNAKE_COLOR)

    snake.squares.insert(0,square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text = "Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if checkCollisions(snake):
        gameOver()
    else:
        window.after(SPEED, nextTurn, snake, food)

def changeDirection(newDirection):
    
    global direction

    if newDirection == "down":
        if direction != "up":
            direction = newDirection
    elif newDirection == "up":
        if direction != "down":
            direction = newDirection
    elif newDirection == "left":
        if direction != "right":
            direction = newDirection
    elif newDirection == "right":
        if direction != "left":
            direction = newDirection

def checkCollisions(snake):
    x,y = snake.coordinates[0]
    if x<0 or x>=GAME_WIDTH:
        return True
    elif y<0 or y>=GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False
def gameOver():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2, font= ("arial",60),text="Game Over", fill = "red", tag = "gameover")


window = Tk()

window.title("Snake Game")

window.resizable(False,False)

score = 0
direction = "down"

label = Label(window, text = "Score:{}".format(score), font = ("arial",40))
label.pack()

canvas = Canvas(window, bg=BG_COLOR,height= GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

window.update()

windowWidth = window.winfo_width()
windowHeight = window.winfo_height()
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

x = int((screenWidth/2)-(windowWidth/2))
y = int((screenHeight/2) - (windowHeight/2))

window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

window.bind("<Up>",lambda event : changeDirection("up"))
window.bind("<Down>",lambda event : changeDirection("down"))
window.bind("<Left>",lambda event : changeDirection("left"))
window.bind("<Right>",lambda event : changeDirection("right"))

snake = Snake()
food = Food()

nextTurn(snake, food)

window.mainloop()