import pygame
import Button
import nimfunction

pygame.init() #initialization 
#SCREEN_WIDTH=16384.999999999998181 #(theoretical limit)
#SCREEN_HEIGHT=16384.999999999998181
SCREEN_WIDTH=1600 #window width and height
SCREEN_HEIGHT=900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #basic parameters for the screen
pygame.display.set_caption('Counting nim') #name of the running program


#getting the images in the first place 
black_circle = pygame.image.load('button.png').convert_alpha()
selected = pygame.image.load('selected.png').convert_alpha()
check = pygame.image.load('check.png').convert_alpha()
uncheck = pygame.image.load('uncheck.png').convert_alpha()
nope = pygame.image.load('nope.png').convert_alpha()
lightbulb_off = pygame.image.load('lightbulb_off.png').convert_alpha()
lightbulb_on = pygame.image.load('lightbulb_on.png').convert_alpha()
add = pygame.image.load('add.png').convert_alpha()
minus = pygame.image.load('minus.png').convert_alpha()


#game variables:
game_menu = True
items_disappear = False
current_set = 0
player_points = 0
computer_points = 0
last_point = 5
game_finished = False
player_turn = True
optimal_computer = False
scoreboard = False


font_big = pygame.font.SysFont("arialblack", 80) #setting a common black font with size 80
font_small = pygame.font.SysFont("arialblack", 40) #common black font size 40
font_smallest = pygame.font.SysFont("arialblack", 20) #size 20
font_tips = pygame.font.SysFont("arialblack", 30)
TEXT_COL = (13,0,128)
TEXT_COL2 = (237, 28, 36)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col) #draw the input 
    screen.blit(img, (x,y))


#creates the buttons:
s=3
c=3
r=6
u = [c*r, c*r, c*r]
items = []
nopes = []
index = 0
for x in range(s): #amount of sets
    for i in range(c): #columns
        for j in range(r): #rows
            items.append(Button.Button(int(335+(i+1)*50+300*x), int(20+(j+1)*50), black_circle, selected, 0.085)) #fill up the list with black items
            items[index].set=x+1 #giving it a "set" value
            index += 1
    nopes.append(Button.Button(int(443+300*x), int(375), nope, nope, 0.15))
    nopes[x].set=x+1

check_button = Button.Button(int(1400), int(665), check, uncheck, 0.2)
lightbulb_button = Button.Button(int(850), int(650), lightbulb_off, lightbulb_on, 0.2)
add_button = Button.Button(int(375), int(350), add, add, 0.2)
minus_button = Button.Button(int(250), int(350), minus, minus, 0.2)

run = True #global value, determines whether the program should run or not (variable, but usually kept away from everything else for clarity)
while run: #the meat and bones, everything that will/can change while playing

    screen.fill((202, 228, 241)) #background color
    key = pygame.key.get_pressed() #get all keyboard inputs


    if key[pygame.K_ESCAPE] == True: #if esc is down
        run = False #shutdown
    #note: not the most elegant way of handling this (I assume), but two "for" loops for the events will make inputs lag and just messing up the program (I assume that high quality project can make it work somehow, but in this case one loop is enough):
    for event in pygame.event.get(): #check ALL events and iterate
        if event.type == pygame.QUIT: #if it's the top right x 
            run = False #shutdown (yes you really need to write a quit option or you can't close the program)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #if you press a key and it's SPACE
                game_menu = not game_menu #change the menu
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn: #PLAYER'S TURN: if it's A mouse button
                for i in range(s*c*r): #for as many items as there are 
                    if current_set == 0 or current_set == items[i-1].set:
                        items[i-1].clicking(pygame.mouse.get_pos()) #get mouse position, execute .clicking function
                        if items[i-1].clicked: #if it was actually clicked
                            current_set = items[i-1].set #lock its set
                check_button.clicking(pygame.mouse.get_pos())
                if check_button.clicked: #clicked the check 
                    items_disappear = True #finalize it
                lightbulb_button.clicking(pygame.mouse.get_pos())
                if lightbulb_button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
                    optimal_computer = not optimal_computer
                add_button.clicking(pygame.mouse.get_pos())
                if add_button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1: #clicked the check 
                    last_point += 1
                minus_button.clicking(pygame.mouse.get_pos())
                if minus_button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1: #clicked the check 
                    last_point -= 1


    if player_turn == False and scoreboard == False: #COMPUTER'S TURN
        if optimal_computer: #smarter algorithm
            pygame.time.delay(1500)
            k, l = nimfunction.best_move(u[0], u[1], u[2], nimfunction.scoring_nim_dp(c*r, last_point), last_point)
            current_set = k+1
            taken = l
            computer_points += taken
            u[k] = u[k] - l
            for i in range(s*c*r):
                if current_set == items[i-1].set and items[i-1].shown and taken != 0:
                    items[i-1].shown = False
                    items[i-1].clicked = False
                    taken -= 1
            current_set = 0
            player_turn = True
        else: #selfish algorithm
            pygame.time.delay(1500)
            current_set = u.index(max(u)) + 1
            taken = nimfunction.selfish_moves(u)
            computer_points += taken
            for i in range(s*c*r):
                if current_set == items[i-1].set:
                    items[i-1].shown = False #disappear
                    items[i-1].clicked = False
            current_set = 0
            player_turn = True

    if game_menu:
        draw_text("Press space to start/resume", font_big, TEXT_COL, 175, 200) #draw the menu text
        draw_text("Press Esc or top right X to shut down", font_small, TEXT_COL, 385, 500)
        if lightbulb_button.clicked:
            draw_text("Smart", font_small, TEXT_COL, 700, 680)
        else:
            draw_text("Selfish", font_small, TEXT_COL, 700, 680)
        lightbulb_button.draw(screen)
        add_button.draw(screen) 
        minus_button.draw(screen) 
        draw_text("Last point: " + str(last_point), font_big, TEXT_COL, 500, 350)
    else:
        draw_text(str(u), font_smallest, TEXT_COL, 721, 20)
        draw_text("Press space to pause", font_big, TEXT_COL, 325, 450) #draw the game text
        pygame.draw.rect(screen, "white", (100, 575, 1200, 275)) #rectangle
        pygame.draw.rect(screen, "black", (100, 575, 1200, 275), 3) #borders
        draw_text("- Click the objects to select them, click again to deselect", font_tips, TEXT_COL, 125, 600)
        draw_text("- Or right click to deselect all", font_smallest, TEXT_COL, 200, 640)
        draw_text("- Click the check button to finalize your choices", font_tips, TEXT_COL, 125, 687)
        draw_text("- Collect more points than the computer (the last one is worth extra)", font_tips, TEXT_COL, 125, 775)

        for i in range(s*c*r): #for the max amount of items
            if items[i-1].clicked and items_disappear == True and scoreboard == 0: #if something is clicked and accepted --> disappear
                items[i-1].shown = False #disappear
                items[i-1].clicked = False
                u[current_set-1] -= 1
                player_points += 1 #give points for every disappeared item
                player_turn = False
            if items[i-1].shown: #if it should be drawn
                items[i-1].draw(screen) #draw them
        check_button.draw(screen) 
        if current_set == 0: #no sets are chosen
            pass
        else:
            for i in range(s): #draw the signs under the right sets
                if nopes[i-1].set != current_set:
                    nopes[i-1].draw(screen)

    draw_text("zsu™", font_smallest, TEXT_COL2, 20, 850)

    #set every game variable back to normal status (if...)
    if not any(b.clicked for b in items): #if none of the items are selected
        current_set = 0 #you can select again from a different (or same) set
    check_button.clicked = False #reset
    items_disappear = False #reset

    #see if the game should end and evaluate the standings 
    if not any(b.shown for b in items) and game_menu != True:
        if player_turn and game_finished == False:
            computer_points += last_point
        elif player_turn == False and game_finished == False:
            player_points += last_point
        game_finished = True
        pygame.draw.rect(screen, (0, 162, 232), (20, 20, 1560, 860))
        draw_text("Player points: " + str(player_points), font_big, TEXT_COL, 300, 200)
        draw_text("Computer points: " + str(computer_points), font_big, TEXT_COL, 300, 400)
        if player_points > computer_points:
            draw_text("You win", font_big, TEXT_COL, 600, 600)
        elif player_points < computer_points:
            draw_text("You lose", font_big, TEXT_COL, 600, 600)
        elif player_points == computer_points:
            draw_text("Draw", font_big, TEXT_COL, 650, 600)
    pygame.display.update() #updates every change above (if you put more it updates more frequently, but at the cost of resources)


pygame.quit() #shuts down the program after the while sequence ends 