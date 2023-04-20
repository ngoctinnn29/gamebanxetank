import pgzrun

WIDTH = 800
HEIGHT = 600
TITLE = "Game Đơn Giản"
game_started = False  # Biến kiểm tra trạng thái bắt đầu game
game_restart = False  # Biến kiểm tra trạng thái chơi lại game

circle_x = WIDTH / 2  # Tọa độ x của vòng tròn
circle_y = HEIGHT / 2  # Tọa độ y của vòng tròn
circle_speed = 3  # Tốc độ di chuyển của vòng tròn

def draw():
    screen.clear()
    if game_started:
        # Vẽ nội dung game
        screen.draw.text("Game đã bắt đầu!", (WIDTH/2 - 100, HEIGHT/2), color="white", fontsize=40)
        screen.draw.circle((circle_x, circle_y), 20, "red")  # Vẽ vòng tròn
    elif game_restart:
        # Vẽ màn hình chơi lại game
        screen.draw.text("Nhấn PHÍM CÁCH để chơi lại", (WIDTH/2 - 250, HEIGHT/2 + 50), color="white", fontsize=30)
    else:
        # Vẽ màn hình bắt đầu
        screen.draw.text("Nhấn PHÍM CÁCH để bắt đầu", (WIDTH/2 - 350, HEIGHT/2), color=(255, 255, 255), fontsize=80)

def update():
    global game_started, game_restart, circle_x, circle_y
    if game_started:
        # Xử lý logic game khi game đã bắt đầu
        circle_x += circle_speed  # Di chuyển vòng tròn theo hướng x
        if circle_x > WIDTH:  # Nếu vòng tròn đi ra khỏi màn hình, đặt lại tọa độ x
            circle_x = 0
    elif game_restart:
        # Kiểm tra nếu người chơi nhấn phím CÁCH, thì bắt đầu game lại
        if keyboard.space:
            game_started = True
            game_restart = False

def on_key_down(key):
    global game_started, game_restart
    if not game_started and key == keys.SPACE:
        # Bắt đầu game khi người chơi nhấn phím CÁCH
        game_started = True
    elif game_restart and key == keys.SPACE:
        # Chơi lại game khi người chơi nhấn phím CÁCH sau khi kết thúc game
        game_started = True
        game_restart = False

pgzrun.go()
