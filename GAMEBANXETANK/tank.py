import pgzrun
import random


WIDTH = 1000
HEIGHT = 600
TANK_SIZE = 25
walls = []
bullets = []
# Định nghĩa biến đếm thời gian giới hạn tốc độ bắn đạn
bullet_cooldown = 0
bullet_cooldown_2 =0
bullet_cooldown_time = 0.5  # Thời gian giới hạn tốc độ bắn đạn (tính bằng giây)

enemy_move_count=0
enemy_bullets = []

enemy_change_direction_count = 0
game_over=False
game_started=False
color_selected=False
enemies =[]
explosions =  []
tanks = []
bricks = []




class Explosion(Actor):
    def __init__(self, x, y):
        super().__init__("explosion3", (x, y))
        self.timer = 0.2 # Thiết lập thời gian sống cho vụ nổ là 0,2 giây

    def update(self):
        self.timer -= 1/60 # Giảm giá trị thời gian sống mỗi khung hình

        # Kiểm tra nếu thời gian sống của vụ nổ đã hết thì xóa đối tượng vụ nổ khỏi danh sách
        if self.timer <= 0:
            explosions.remove(self)


# dịnh dạng xe tănng mình
class Tank(Actor):
    def __init__(self, image, x, y):
        super().__init__(image, (x, y))
        
x = WIDTH / 2
y = HEIGHT - TANK_SIZE
tank = Tank("tank_blue",x ,y)
tank.angle = 90

explostion = Actor("explosion4")

def on_key_down(key):
    global tank
    if key == keys.R:
        tank.image = "tank_red"
    elif key == keys.B:
        tank.image = "tank_blue"
    elif key == keys.G:
        tank.image = "tank_green"

# background và tường 
background_1 = Actor('bg')
background = Actor('grass')
for x in range(20):
    for y in range(15): #lặp trục x y
        if random.randint(0, 50) < 20: #tạo ngẫu nhiên các block không quá 20
            wall = Actor('wall')
            # Đặt các tường không chắn ngang giữa màn hình
            if x % 2 == 0:
                wall.x = x * 50 + TANK_SIZE
                wall.y = y * 50 + TANK_SIZE * 3
            else:
                wall.x = x * 50 + TANK_SIZE
                wall.y = y * 50 + TANK_SIZE * 3
            # Đặt các tường không đè lên vị trí khởi đầu của xe tank
            if wall.colliderect(tank):
                continue
            walls.append(wall)
        elif random.randint(0, 50) < 20:
            # Tạo các viên gạch không trùng lên vị trí của các tường đã có
            brick = Actor('brick')
            brick.x = x * 50 + TANK_SIZE
            brick.y = y * 50 + TANK_SIZE * 3
            if brick.colliderect(tank):
                continue
            if any(brick.colliderect(wall) for wall in walls):
                continue
            bricks.append(brick)
#định dạng xe tăng địch 
class EnemyTank(Actor):
    def __init__(self, image, x, y):
        super().__init__(image, (x, y))
        self.angle = 270

for i in range (4):
    enemy = EnemyTank("tank_red", x, y)
    enemy.x=i *200+100
    enemy.y=TANK_SIZE
    enemies.append(enemy)

def tank_set():
    global tank
    original_x=tank.x
    original_y=tank.y
    speed = 2 # Tốc độ di chuyển của xe tăng
    if keyboard.left:
        tank.x -= speed # Di chuyển sang trái
        tank.angle = 180 # Cập nhật góc quay của xe tăng là 180 độ (quay về phía trái)
    if keyboard.right:
        tank.x += speed # Di chuyển sang phải
        tank.angle = 0 # Cập nhật góc quay của xe tăng là 0 độ (quay về phía phải)
    if keyboard.up:
        tank.y -= speed # Di chuyển lên trên
        tank.angle = 90 # Cập nhật góc quay của xe tăng là 270 độ (quay về phía trên)
    if keyboard.down:
        tank.y += speed # Di chuyển xuống dưới
        tank.angle = 270 # Cập nhật góc quay của xe tăng là 90 độ (quay về phía dưới)
    
    if tank.collidelist(walls)!=-1:
        tank.x=original_x
        tank.y=original_y
    if tank.x<TANK_SIZE or tank.x>(WIDTH-TANK_SIZE) or tank.y<TANK_SIZE or tank.y>(HEIGHT-TANK_SIZE):
        tank.x=original_x
        tank.y=original_y
    if tank.collidelist(bricks)!=-1:
        tank.x=original_x
        tank.y=original_y
    if tank.x<TANK_SIZE or tank.x>(WIDTH-TANK_SIZE) or tank.y<TANK_SIZE or tank.y>(HEIGHT-TANK_SIZE):
        tank.x=original_x
        tank.y=original_y

def tank_bullets_set(): # set up về đạn xe tăng phe mình 
    global bullet_cooldown

    if keyboard.space and bullet_cooldown <= 0:
        bullet = Actor("bulletblue2")
        bullet.angle = tank.angle
        bullet.pos = tank.pos
        bullets.append(bullet)
        bullet_cooldown = bullet_cooldown_time  # Đặt lại biến đếm thời gian

    for bullet in bullets:
        if bullet.angle == 0:
            bullet.x += 5
        elif bullet.angle == 180:
            bullet.x -= 5
        elif bullet.angle == 90:
            bullet.y -= 5
        elif bullet.angle == 270:
            bullet.y += 5

    bullet_cooldown -= 1/60  # Giảm giá trị biến đếm thời gian theo tốc độ khung hình (60 khung hình/giây)
    for bullet in bullets:
        bricks_index = bullet.collidelist(bricks)
        if bricks_index != -1:
            sounds.exp.play()
            bullets.remove(bullet)
        walls_index = bullet.collidelist(walls)
        if walls_index != -1:  # Kiểm tra đạn có va chạm với tường không
            sounds.gun9.play()
            del walls[walls_index]
            bullets.remove(bullet)
        if bullet.x<0 or bullet.x>WIDTH or bullet.y<0 or bullet.y>HEIGHT:
            bullets.remove(bullet)
        enemy_index=bullet.collidelist(enemies) # khi bắn trúng xe địch sẽ phá huỷ tank địch
        if enemy_index!=-1:
            sounds.exp.play()
            explosion = Explosion(enemies[enemy_index].x, enemies[enemy_index].y)
            explosions.append(explosion)
            bullets.remove(bullet)
            del enemies[enemy_index] 
def enemy_set():
    global enemy_move_count, bullet_cooldown_2,enemy_change_direction_count
    for enemy in enemies:
        original_x=enemy.x
        original_y=enemy.y
        choice=random.randint(0,2)
        if enemy_move_count>0:
            enemy_move_count=enemy_move_count -1
            if enemy.angle==0:
                enemy.x=enemy.x+2
            elif enemy.angle==180:
                enemy.x=enemy.x-2
            elif enemy.angle==90:
                enemy.y=enemy.y-2
            elif enemy.angle==270:
                enemy.y=enemy.y+2
            if enemy.collidelist(walls)!=-1:
                enemy.x=original_x
                enemy.y=original_y
            if enemy.collidelist(bricks)!=-1:
                enemy.x=original_x
                enemy.y=original_y
            if enemy.x<TANK_SIZE or enemy.x>(WIDTH-TANK_SIZE) or enemy.y<TANK_SIZE or enemy.y>(HEIGHT-TANK_SIZE):
                enemy.x=original_x
                enemy.y=original_y
                
        if choice==0:   # xe tăng địch di chuyển 
            enemy_move_count=1
        if choice==1: # xe tăng địch đổi hướng 
            if enemy_change_direction_count > 0:
                enemy_change_direction_count -= 1
            else:
                # Đổi hướng
                enemy.angle = random.randint(0,3)*90
                enemy_change_direction_count = 10 # Đổi hướng sau 10 lần di chuyển
        else:       # xe tăng địch bắn 
            if bullet_cooldown_2==0:
                bullet=Actor("bulletred2")
                bullet.angle = enemy.angle
                bullet.pos=enemy.pos
                enemy_bullets.append(bullet)
                bullet_cooldown_2=50
            else:
                bullet_cooldown_2 =bullet_cooldown_2-1
        
def enemy_bullets_set(): 
    global enemies , game_over 
    for bullet in enemy_bullets:
        if bullet.angle == 0:
            bullet.x += 5
        elif bullet.angle == 180:
            bullet.x -= 5
        elif bullet.angle == 90:
            bullet.y -= 5
        elif bullet.angle == 270:
            bullet.y += 5

    # đạn địch phá tường phá xe 
    for bullet in enemy_bullets:
        brick_index=bullet.collidelist(bricks)
        if brick_index!=-1:
            sounds.exp.play()
        wall_index=bullet.collidelist(walls)
        if wall_index!=-1:
            sounds.gun10.play()
            del walls[wall_index]
            enemy_bullets.remove(bullet)
        if bullet.x<0 or bullet.x>WIDTH or bullet.y<0 or bullet.y>HEIGHT:
            enemy_bullets.remove(bullet)
        if bullet.colliderect(tank):
            sounds.exp.play()
            game_over=True
            enemies=[]



def update(): 
    global game_over, game_started
    if game_started:
        tank_set()
        tank_bullets_set()
        enemy_set()
        enemy_bullets_set()
        
def on_key_down(key):
    global game_started, tank, color_selected
    if not game_started and key == keys.SPACE:
        # Bắt đầu game khi người chơi nhấn phím SPACE
        game_started = True
    elif game_started and not color_selected:
        if key == keys.R:
            tank.image = "tank_red"
            color_selected = True
        elif key == keys.B:
            tank.image = "tank_blue"
            color_selected = True
        elif key == keys.G:
            tank.image = "tank_green"
            color_selected = True
    elif color_selected and key == keys.SPACE:
        # Reset lại biến color_selected khi người chơi nhấn phím SPACE sau khi đã chọn màu
        color_selected = False


    
def draw():
    global color_selected
    background_1.draw()
    if not game_started:
        # Vẽ màn hình bắt đầu
        screen.draw.text("enter SPACE to begin!!", (WIDTH/2-325, HEIGHT-100), color="white", fontsize=80)
    elif color_selected:
        # Vẽ màn hình chọn màu
        screen.fill((0, 0, 0))
        screen.draw.text("Choose tank color:", (WIDTH/2-200, HEIGHT/2-200), color="white", fontsize=60)
        screen.draw.text("Press R for Red", (WIDTH/2-100, HEIGHT/2-100), color="red", fontsize=40)
        screen.draw.text("Press B for Blue", (WIDTH/2-100, HEIGHT/2), color="blue", fontsize=40)
        screen.draw.text("Press G for Green", (WIDTH/2-100, HEIGHT/2+100), color="green", fontsize=40)
    else:
        # Vẽ trạng thái của trò chơi
        if game_over:
            screen.fill((0,0,0))
            screen.draw.text("YOU LOSE", (300, 250), color=(255, 255, 255), fontsize=100)
        elif len(enemies) == 0:
            screen.fill((0,0,0))
            screen.draw.text("YOU WIN", (300, 250), color=(255, 255, 255), fontsize=100)
        else:
            background.draw()
            tank.draw()
            for explosion in explosions:
                explosion.draw()
                explosion.update()
            for wall in walls:
                wall.draw()
            for brick in bricks:
                brick.draw()
            for bullet in bullets:
                bullet.draw()
            for enemy in enemies:
                enemy.draw()
            for bullet in enemy_bullets:
                bullet.draw()


pgzrun.go()

