from itertools import cycle
from random import randrange
from tkinter import Tk, Canvas, messagebox, font, PhotoImage
import random
import cv2

canvas_width = 800
canvas_height = 400

win = Tk()
c = Canvas(win , width = canvas_width , height = canvas_height, background = 'deep sky blue')
c.create_rectangle(-5, canvas_height-100, canvas_width + 5, canvas_height + 5, fill='green', width=0)
c.create_oval(-80,-80,120,120,fill='orange', width=0)
c.pack()

images = ["img/black.png","img/white.png", "img/brown.png"]
cat_width = 50
cat_height = 50
cat_interval = 4000
cat_speed = 500
cat_score = 20
dificulty_factor = 0.95

catcher_color = 'blue'
catcher_width=  100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width/ 2
catcher_start_y = canvas_height - catcher_height - 20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

catcher = c.create_arc(catcher_start_x,catcher_start_y,catcher_start_x2,catcher_start_y2, start=200, extent = 140, style = 'arc', outline=catcher_color, width = 3)

score = 0
score_text = c.create_text(10,10,anchor='nw',font=('Arial',18,'bold'),fill='darkblue', text='Score: ' + str(score))

lives_remaning = 3
lives_text =c.create_text(canvas_width-10,10,anchor='ne',font=('Arial',18,'bold'),fill='darkblue', text='Lives: ' + str(lives_remaning))

cats = []
tab1 = []
def create_cats():
    #img = PhotoImage(file=random.choice(images))
    img = cv2.imread(random.choice(images), cv2.IMREAD_UNCHANGED)
    img2 = cv2.resize(img,(cat_width,cat_height))
    cv2.imwrite("img/resize.png", img2)
    img_res = PhotoImage(file="img/resize.png")
    tab1.append(img_res)
    x = randrange(10,740)
    y = 40
    new_cat = c.create_image(x,y,image=tab1[-1])
    cats.append(new_cat)
    win.after(cat_interval,create_cats)

def move_cats():
    for cat in cats:
        (x,y) = c.coords(cat)
        c.move(cat,0,10)
        if y > canvas_height:
            cat_dropped(cat)
    win.after(cat_speed,move_cats)

def cat_dropped(cat):
    cats.remove(cat)
    c.delete(cat)
    lose_a_life()
    if lives_remaning == 0:
        messagebox.showinfo('GAME OVER', 'Final Score: ' + str(score))
        win.destroy()

def lose_a_life():
    global lives_remaning
    lives_remaning -= 1
    c.itemconfigure(lives_text, text='Lives : ' + str(lives_remaning))

def catch_check():
    (catcher_x,catcher_y,catcher_x2,catcher_y2) = c.coords(catcher)
    for cat in cats:
        (x,y) = c.coords(cat)
        if (x-cat_width/2) > catcher_x and (x+cat_width/2) < catcher_x2 and catcher_y+50 < (y+cat_height/2):
            cats.remove(cat)
            c.delete(cat)
            increase_score(cat_score)
    win.after(100,catch_check)

def increase_score(points):
    global score , cat_speed , cat_interval
    score += points
    cat_speed = int(cat_speed * dificulty_factor)
    cat_interval = int(cat_interval * dificulty_factor)
    c.itemconfigure(score_text,  text = 'Score : ' + str(score))

def move_left(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher,-20,0)

def move_right(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher,20,0)

c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.focus_set()

win.after(1000,create_cats)
win.after(1000,move_cats)
win.after(1000,catch_check)

win.mainloop()
