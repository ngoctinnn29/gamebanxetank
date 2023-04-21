import pgzrun

WIDTH = 800
HEIGHT = 600
TANK_SIZE = 64

tank = Actor("tank_blue")
tank.pos = (WIDTH/2 , HEIGHT-TANK_SIZE)
tank.angle = 90

def draw():
    screen.fill("black")
    tank.draw()

def update():
    pass

def on_key_down(key):
    global tank
    if key == keys.R:
        tank.image = "tank_red"
    elif key == keys.B:
        tank.image = "tank_blue"
    elif key == keys.G:
        tank.image = "tank_green"

pgzrun.go()
