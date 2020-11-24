import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 850))
    screen.blit(floor_surface, (floor_x_pos + 576, 850))

def create_hook():
    random_hook_pos = random.choice(hook_height)
    bottom_hook = hook_surface.get_rect(midtop = (700, random_hook_pos)) #midtop is placed at this point of screen, 700 so they come from outside
    top_hook = hook_surface.get_rect(midbottom = (700, random_hook_pos - 300))
    return bottom_hook, top_hook

def move_hooks(hooks):
    #uses the list to get hooks and move them at the same time to the left
    for hook in hooks:
        hook.centerx -= 5
    visible_hooks = [hook for hook in hooks if hook.right > -50] #only stores hooks that are on the screen in the list
    return visible_hooks

def draw_hooks(hooks):
    for hook in hooks:
        if hook.bottom >= 924:
            screen.blit(hook_surface, hook)
        else:
            flip_hook = pygame.transform.flip(hook_surface, False, True)
            screen.blit(flip_hook, hook)

#controls whether game is displaying assets/continues
def check_collison(hooks):
    global can_score  #influencing variable outside of this f(x)
    for hook in hooks:
        if gary_rect.colliderect(hook):
            death_sound.play()
            can_score = True
            return False
    if gary_rect.top <= -100 or gary_rect.bottom >= 900: #have to use < and > instead of = since you wont get exact pixel measurments
       can_score = True
       return False

    return True

def rotate_gary(gary):
    new_gary = pygame.transform.rotozoom(gary, -gary_movement * 3, 1)
    return new_gary

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,700))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def hook_score_check():
    global can_score, score
    if hook_list:
        for hook in hook_list:
            if 95 < hook.centerx < 105 and can_score: #100 is the position of Gary, and use < for wiggle room
                score += 1
                score_sound.play()
                can_score = False
            if hook.centerx < 0: #once hook moves past 0, score can increase again
                can_score = True
#so the audio doesnt lag behind/wait for buffer
#pygame.mixer.pre_init(frequency=44100, size = 16, channels = 1, buffer=256)
pygame.init()
screen = pygame.display.set_mode((576, 924))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

#Game Variables
gravity = 0.25
gary_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('assets/Bikini-bottom.jpg').convert()
bg_surface = pygame.transform.scale(bg_surface, (900, 924))

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

gary_surface = pygame.image.load('assets/smile_gary.png').convert_alpha()
gary_surface = pygame.transform.scale(gary_surface, (70,60))
gary_rect = gary_surface.get_rect(center = (100, 70))

hook_surface = pygame.image.load('assets/fish_hook.png').convert_alpha()
hook_surface = pygame.transform.scale(hook_surface, (130,900))
hook_list = []
SPAWNHOOK = pygame.USEREVENT
pygame.time.set_timer(SPAWNHOOK, 1200)
hook_height = [300,500,700]

game_over_surface = pygame.image.load('assets/start_screen.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (288,462))

swim_sound = pygame.mixer.Sound('sound/swimming.mp3')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                gary_movement = 0 #make sure the jumps are the exact same height
                gary_movement -= 9
                swim_sound.play()
            #restarting game
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                hook_list.clear()
                gary_rect.center = (100, 512)
                gary_movement = 0
                score = 0 #so that the score isn't always increasing
        if event.type == SPAWNHOOK:
            hook_list.extend(create_hook()) #extend tuple with two elements from create_hook
    screen.blit(bg_surface,(0,0))

    if game_active:
        #Gary
        gary_movement +=gravity
        rotated_gary = rotate_gary(gary_surface)
        gary_rect.centery += gary_movement
        screen.blit(rotated_gary, gary_rect)
        game_active = check_collison(hook_list)

        #Hooks
        hook_list = move_hooks(hook_list)
        draw_hooks(hook_list)
        #score += 0.01 #takes 100 cycles to get to 1
        #score
        hook_score_check()
        score_display('main_game')
        #score_sound_countdown -= 1
        #if score_sound_countdown <= 0:
            #score_sound.play()
            #score_sound_countdown = 100 #takes 100 cycles to get to 0
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    #Floor
    floor_x_pos -= 1
    draw_floor()
    #make floor continuous
    if floor_x_pos <= -576:
        floor_x_pos = 0
    
    
    pygame.display.update() #draws anything in while loop on screen variable
    clock.tick(120)