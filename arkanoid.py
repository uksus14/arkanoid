import pygame as pg
from math import hypot, sin, cos, pi
from random import randrange, random
from json import dumps, loads
from pygame.locals import *
pg.font.init()
pg.mixer.init()

WIDTH, HEIGHT = 900, 800
STANDART_FONT = "static/Pixel.ttf"
TEXT_COLOR = (255, 255, 255)
BLOCKSIZE = 30
fps = 120



with open("static/levels.json", "r") as f: data = loads(f.read())
levels = data

def allow_to_place(point, rect):
    Cent1, Cent2 = point, [rect[0]+BLOCKSIZE/2, rect[1]+BLOCKSIZE/2]
    dx, dy = [abs(Cent1[i]-Cent2[i])-BLOCKSIZE for i in [0,1]]
    return dy>0 or dx>0

def allow_to_delete(point, rect):
    Cent = [rect[0]+BLOCKSIZE/2, rect[1]+BLOCKSIZE/2]
    dx, dy = [abs(Cent[i]-point[i])-BLOCKSIZE/2 for i in [0,1]]
    return dy<0 and dx<0

def get_font(size, text, x, y, color = TEXT_COLOR, style=STANDART_FONT):
    text_surface = pg.freetype.Font(style, size).render(text, color)
    sc.blit(text_surface[0], (x, y))

def editor_update(block_list, is_saved):
    sc.blit(bg_texture, (0, 0))
    get_font(15,"Click lmb somewhere to create block", 100, 625)
    get_font(15,"Click rmb on block to delete it", 100, 650)
    get_font(15,"Press 'C' to clear all blocks", 100, 675)
    get_font(15,"Press Enter to save layout", 100, 700)
    if is_saved:
        get_font(15,"Saved!", 700, 700)
    # drawing world
    [sc.blit(block_texture, (block[0], block[1])) for block in block_list]
    pg.display.flip()
    

def editor_loop(layout):
    is_saved = True
    creating = True
    placing = False
    clearing = False
    saved_layout = layout.copy()
    while creating:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == QUIT:
                return "close program"
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    creating = False
                elif event.key == K_c:
                    is_saved = False
                    layout.clear()
                elif event.key == K_RETURN:
                    is_saved = True
                    saved_layout = layout.copy()
            elif event.type == MOUSEBUTTONDOWN:
                clearing = event.button-1
                placing = event.button-3
            elif event.type == MOUSEBUTTONUP:
                placing, clearing = False, False
        if placing:
            x, y = pg.mouse.get_pos()
            if min(WIDTH-x, x)>BLOCKSIZE/2 and min(HEIGHT-y, y)>BLOCKSIZE/2:
                if all([allow_to_place([x, y], block) for block in layout]):
                    is_saved = False
                    layout.append([x-BLOCKSIZE/2, y-BLOCKSIZE/2])
        elif clearing:
            x, y = pg.mouse.get_pos()
            for block_id, block in enumerate(layout):
                if allow_to_delete([x, y], block):
                    del layout[block_id]
                    is_saved = False
                    break

        editor_update(layout, is_saved)
    return saved_layout


def editor():
    level = 0
    creating, run_program = False, True
    while run_program:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == QUIT:
                run_program = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run_program = False
                elif event.key == K_SPACE:
                    creating = True
                elif event.key == K_0:level = 0
                elif event.key == K_1:level = 1
                elif event.key == K_2:level = 2
                elif event.key == K_3:level = 3
                elif event.key == K_4:level = 4
                elif event.key == K_5:level = 5
                elif event.key == K_6:level = 6
                elif event.key == K_7:level = 7
                elif event.key == K_8:level = 8
                elif event.key == K_9:level = 9

        sc.blit(bg_texture, (0, 0))
        get_font(30, "Welcome to Level editor", 270, 70)
        get_font(20, f"Now editing level {level}", 350, 150)
        get_font(20, "Choose level by pressing a number button", 100, 600)
        get_font(20, "Press space to edit", 100, 650)
        get_font(15, "press esc to exit", 700, 700)
        keys = pg.key.get_pressed()
        pg.display.update()


        if creating:
            creating = False
            answer = editor_loop(levels[level])
            if answer == "close program":
                run_program = False
            levels[level] = answer
    with open("static/levels.json", "w") as f: f.write(dumps(levels))
    return levels


# platform settings
platform_w = 180
platform_h = 28
platform_speed = 8
# sphere settings
sphere_radius = 15
speed = 300/fps
sphere_speed = 2**0.5
level = 0
# blocks settings

balls = 5
current_skin = 0
skin_button = pg.Rect(80, 650, 200, 100)
platform, sphere_rect, sphere, dx, dy = [1]*5
def setup():
    global platform, sphere_rect, sphere, dx, dy
    # angle = pi*(10*random()+1)/12
    # spawn = randrange(sphere_radius, WIDTH - sphere_radius)
    spawn=165
    angle=pi/2
    dx, dy = cos(angle)*sphere_speed, -sin(angle)*sphere_speed
    platform = pg.Rect(WIDTH/2-platform_w/2, HEIGHT - platform_h - 10, platform_w, platform_h)
    sphere_rect = int(sphere_radius * 2 ** 0.5)
    sphere = pg.Rect(spawn, HEIGHT // 2, sphere_rect, sphere_rect)
first_level = [(10 + 140 * i, 10 + 70 * j) for i in range(10) for j in range(4)]
collision_sound = pg.mixer.Sound("static/collision.mp3")
lose_sound = pg.mixer.Sound("static/lose.mp3")
win_sound = pg.mixer.Sound("static/win.mp3")
def change_music(music):
    pg.mixer.music.load(f"static/{music}_music.mp3")
    pg.mixer.music.play(-1)


pg.init()
sphere_after = sphere
clock = pg.time.Clock()
sc = pg.display.set_mode((WIDTH, HEIGHT))

# background image
button_texture = pg.transform.scale(pg.image.load("static/button.png").convert_alpha(), skin_button.size)
block_texture = pg.transform.scale(pg.image.load("static/block.png").convert_alpha(), (BLOCKSIZE, BLOCKSIZE))
playing_bg_texture = pg.transform.scale(pg.image.load("static/playing_menu_bg.jpg").convert_alpha(), (WIDTH, HEIGHT))
bg_texture = pg.transform.scale(pg.image.load("static/menu_bg.jpg").convert_alpha(), (WIDTH, HEIGHT))
platform_texture = pg.transform.scale(pg.image.load("static/platform.png").convert_alpha(), (platform_w, platform_h))
ball_textures = [pg.transform.scale(pg.image.load(f"static/ball{i}.png").convert_alpha(), (sphere_radius*2, sphere_radius*2)) for i in range(balls)]

def change_skin():
    global current_skin
    while True:
        clock.tick(fps)
        previous = pg.transform.scale(pg.image.load(f"static/ball{current_skin-1}.png").convert_alpha(), (sphere_radius*6, sphere_radius*6))
        current = pg.transform.scale(pg.image.load(f"static/ball{current_skin}.png").convert_alpha(), (sphere_radius*6, sphere_radius*6))
        next = pg.transform.scale(pg.image.load(f"static/ball{current_skin+1}.png").convert_alpha(), (sphere_radius*6, sphere_radius*6))
        sc.blit(bg_texture, (0, 0))
        sc.blit(previous, (2*WIDTH/6-sphere_radius*3, HEIGHT/3))
        sc.blit(current, (3*WIDTH/6-sphere_radius*3, HEIGHT/3))
        sc.blit(next, (4*WIDTH/6-sphere_radius*3, HEIGHT/3))
        get_font(30, "Press Space to submit", 250, 600)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and current_skin>0:
                    current_skin -= 1
                elif event.key == K_RIGHT and current_skin+1<balls:
                    current_skin += 1
                elif event.key == K_SPACE:
                    return 0

def circ_rect_distance(circ, rect):
    Cent = rect.center
    circ_cent = circ.center
    Exten = list(map(lambda x:x/2, rect.size))
    dx, dy = [max(0, abs(circ_cent[j]-Cent[j])-Exten[j]) for j in [0,1]]
    return hypot(dx, dy)-sphere_radius

def platform_collision(dx, dy, sphere, rect, level):
    dist = circ_rect_distance(sphere, rect)

    sphere_after = pg.Rect(sphere.x + (speed+level) * dx , sphere.y + (speed+level) * dy, sphere_rect, sphere_rect)
    if dist<=10:
        if circ_rect_distance(sphere_after, rect)<=dist:
            if sphere.bottom>=rect.top:
                if rect.centerx == sphere.centerx:
                    dx = 0
                    dy = -sphere_speed
                else:
                    ratio = platform_w/(rect.centerx - sphere.centerx)
                    check = 1
                    if ratio <= 0: check = -1
                    ratio = abs(ratio)
                    angle = 1/ratio**0.55+pi/2
                    dy = -sin(angle)*sphere_speed
                    dx = check*cos(angle)*sphere_speed
    return dx, dy

def block_collision(dx, dy, sphere, rect):
    print(rect.centerx, sphere.centerx)
    if abs(sphere.centerx-rect.centerx)<rect.width/2:
        return dx, -dy
    if abs(sphere.centery-rect.centery)<rect.height/2:
        return -dx, dy
    dot = min(map(lambda x:(abs(sphere.centerx-x),x),(rect.right,rect.left)))[1], min(map(lambda y:(abs(sphere.centery-y),y),(rect.height,rect.bottom)))[1]
    mx, my = sphere.centerx-dot[0], sphere.centery-dot[1]
    h=(mx**2+my**2)**0.5
    mx, my = mx/h, my/h
    c=2*(dx*mx+dy*my)
    print((dx, dy))
    print((mx, my))
    dx, dy = dx-c*mx, dy-c*my
    print((dx, dy))
    return dx, dy

def endgame(block_list):
    message = "You won!"
    if block_list:
        message = "You lose :("
        lose_sound.play()
    else:
        win_sound.play()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return -1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return not block_list
        sc.blit(playing_bg_texture, (0, 0))
        get_font(45, message, 350, 300)
        get_font(15,"press esc to go to menu", 700, 700)
        [sc.blit(block_texture, (block.left, block.top)) for block in block_list]
        sc.blit(platform_texture, (platform.left, platform.top))
        sc.blit(ball_textures[current_skin], (sphere.left, sphere.top))
        pg.display.flip()


def update(block_list):
    sc.blit(playing_bg_texture, (0, 0))
    get_font(15,"press esc to go to menu", 650, 700)
    # drawing world
    [sc.blit(block_texture, (block.left, block.top)) for block in block_list]
    sc.blit(platform_texture, (platform.left, platform.top))
    sc.blit(ball_textures[current_skin], (sphere.left, sphere.top))
    pg.display.flip()
    

def mainloop(block_list, level):
    global dx, dy
    setup()
    change_music("main")
    while block_list:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == QUIT:
                return -1
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 0
        # sphere movement
        sphere.x += (speed+level) * dx
        sphere.y += (speed+level) * dy
        # collision left right
        if sphere.centerx < sphere_radius:
            dx = abs(dx)
        if sphere.centerx > WIDTH - sphere_radius:
            dx = -abs(dx)
        # collision top
        if sphere.centery < sphere_radius:
            dy = abs(dy)
        # collision platform
        if sphere.colliderect(platform) and dy > 0:
            collision_sound.play()
            dx, dy = platform_collision(dx, dy, sphere, platform, level)
        hit_index = sphere.collidelist(block_list)
        if hit_index+1:
            collision_sound.play()
            hit_rect = block_list.pop(hit_index)
            dx, dy = block_collision(dx, dy, sphere, hit_rect)
        if not block_list:
            return endgame([])
        if sphere.bottom > HEIGHT:
            return endgame(block_list)
    
        # control
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] and platform.left > 0:
            platform.left -= (platform_speed+level*2)
        if key[pg.K_RIGHT] and platform.right < WIDTH:
            platform.right += (platform_speed+level*2)
        # update screen
        update(block_list)
    return endgame(block_list)


def menu():
    global dx, dy, levels
    change_music("menu")
    level = 0
    playing, run_program = False, True
    levels_passed = []
    setup()
    while run_program:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == QUIT:
                run_program = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run_program = False
                if event.key == K_SPACE:
                    playing = True
                if event.key == K_e:
                    levels = editor()
                elif event.key == K_0:level = 0
                elif event.key == K_1:level = 1
                elif event.key == K_2:level = 2
                elif event.key == K_3:level = 3
                elif event.key == K_4:level = 4
                elif event.key == K_5:level = 5
                elif event.key == K_6:level = 6
                elif event.key == K_7:level = 7
                elif event.key == K_8:level = 8
                elif event.key == K_9:level = 9
            if event.type == MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if circ_rect_distance(pg.Rect(x-1, y-1, 2, 2), skin_button)<2:
                    change_skin()
        sphere.x += (speed+level) * dx
        sphere.y += (speed+level) * dy
        if sphere.centerx < sphere_radius:         dx = abs(dx)
        if sphere.centerx > WIDTH - sphere_radius: dx = -abs(dx)
        if sphere.centery < sphere_radius:         dy = abs(dy)
        if sphere.centery > HEIGHT - sphere_radius:dy = -abs(dy)

        sc.blit(bg_texture, (0, 0))
        sc.blit(ball_textures[current_skin], (sphere.left, sphere.top))
        sc.blit(button_texture, skin_button.topleft)
        get_font(20, "Change skin", skin_button.left+25, skin_button.top+40)
        get_font(30, f"level {level}", 400, HEIGHT/2)
        if level in levels_passed:get_font(30, f"passed", 395, HEIGHT/2+50)
        get_font(30, "Welcome to Arkanoid!", 300, 70)
        get_font(30, "Press space to start", 300, 252)
        get_font(15, "press 'E' to enter editor mode", 80, 600)
        get_font(15, "press esc to exit", 700, 700)
        keys = pg.key.get_pressed()
        pg.display.update()



        if playing:
            playing = False
            block_list = [pg.Rect(block[0], block[1], BLOCKSIZE, BLOCKSIZE) for block in levels[level]]
            answer = mainloop(block_list, level)
            if answer == -1:
                run_program = False
            elif answer:
                levels_passed.append(level)
                level = (level+1)%10
            change_music("menu")

menu()
exit()
