import pygame as pg
from pygame.locals import *
from tris_ai  import alpha_beta_pruning

#Dimensions of the window
HEIGHT = 600
WIDTH = 800

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Positions of the squares of the grid
CENTER = (WIDTH // 2, HEIGHT // 2)
TOP = (WIDTH // 2, HEIGHT // 3)
BOTTOM = (WIDTH // 2, HEIGHT // 2 + HEIGHT // 6)
TOP_LEFT = (WIDTH // 3, TOP[1])
CENTER_LEFT = (TOP_LEFT[0], CENTER[1])
BOTTOM_LEFT = (TOP_LEFT[0], BOTTOM[1])
TOP_RIGHT = (WIDTH // 6 + WIDTH //2, TOP[1])
CENTER_RIGHT = (TOP_RIGHT[0], CENTER[1])
BOTTOM_RIGHT = (TOP_RIGHT[0], BOTTOM[1])

#Collects all the possible position
POSITIONS = [
    [TOP_LEFT, TOP, TOP_RIGHT],
    [CENTER_LEFT, CENTER, CENTER_RIGHT],
    [BOTTOM_LEFT, BOTTOM, BOTTOM_RIGHT]]

#Inner state of the grid (0=empty square, O or X = checked square)
tris = [[0,0,0],
        [0,0,0],
        [0,0,0]]

#Check if the game is over
#returns true, res if it's over (res = "X wins" or "Draw" or "O wins")
#resturns false, "" otherwise
def is_ended(mat):
    result = "Draw"
    w = " wins"
    end = True 
    n = range(3)

    #if there is at least one empty square the game is not over
    for i in n:
        for j in n:
            if mat[i][j] == 0:
                end = False
    
    #if there are three same elements on the same raw the game is over 
    for x in mat:
        if x[0] == x[1] and x[0] == x[2] and x[0] != 0:   
            end = True 
            result = x[0] + w
            break
    
    #if there are three same elements on the same column the game is over 
    for i in n:
        if mat[1][i] == mat[2][i] and mat[0][i] == mat[1][i] and mat[0][i] != 0:
            end = True
            result = mat[0][i] + w
            break
    
    #if there are three same elements on the same diagonal the game is over 
    if ((mat[0][0] == mat[1][1] and mat[0][0] == mat[2][2]) or (mat[0][2] == mat[1][1] and mat[1][1] == mat[2][0])) and mat[1][1] != 0:
        end = True
        result = mat[1][1] + w 
    
    return end, result

#Draws a circle (10 pixel thic) on the surface screen, with center as its center
def draw_o(screen, center):
    pg.draw.circle(screen, WHITE, center, 40)
    pg.draw.circle(screen, BLACK, center, 30)
    pg.display.flip()

#Draws an X (10 pixel thic) on the surface screen, with center as its center
def draw_x(screen, center):
    pg.draw.line(screen, WHITE, (center[0]-25, center[1]-25), (center[0]+25, center[1]+25), 10)
    pg.draw.line(screen, WHITE, (center[0]+25, center[1]-25), (center[0]-25, center[1]+25), 10)
    pg.display.flip()
    
#Draws the tic tac toe grid on the surface screen
def draw_grid(screen) :
    left_vertical = pg.Rect(WIDTH // 2 -70, 150, 10, HEIGHT // 2)
    right_vertical = pg.Rect(WIDTH // 2 +60, 150, 10, HEIGHT // 2)
    top_horiz = pg.Rect(WIDTH // 4, HEIGHT // 2 - 50, WIDTH // 2, 10)
    bottom_horiz = pg.Rect(WIDTH // 4, HEIGHT // 2 + 50, WIDTH // 2, 10)

    pg.draw.rect(screen, WHITE, left_vertical)
    pg.draw.rect(screen, WHITE, right_vertical)
    pg.draw.rect(screen, WHITE, top_horiz)
    pg.draw.rect(screen, WHITE, bottom_horiz)
    pg.display.flip()

#Draws O or X depending on the TURN the game is in on the surface screen
# row = row of the grid
# col = column of the grid 
#Sets the position [row][col] of the grid to X or O depending on char
def draw(screen,row, col, char):
    if char == 'O':
        draw_o(screen, POSITIONS[row][col])
        tris[row][col] = char
    elif char == 'X' :
        draw_x(screen, POSITIONS[row][col])
        tris[row][col] = char

#Handle the mouse click by drawing O or X depending on the TURN[0], in the position of the click
#Draws only if the click is on a empty square of the grid
def handle_click(screen, ev, char) :
    hlength = 400 // 3
    vlength = 100
    x=None
    y=None
    for i in range(3):
        if 200 + i*hlength<=ev.pos[0] and ev.pos[0] <= (i+1)*hlength + 200:
            y =i
    for i in range(3):
        if 150 + i*vlength<=ev.pos[1] and ev.pos[1] <= (i+1)*vlength + 200:
            x=i

    if x !=None and y!=None and tris[x][y] == 0:
        draw(screen, x, y, 'X')
        _ , ac = alpha_beta_pruning(tris)
        if tris[ac//3][ac%3] == 0:
            draw(screen, ac//3, ac%3, 'O')


#Resets the game by setting to 0 the TURN and clearing the grid
def reset():
    for x in tris:
        for i in range(3):
            x[i] = 0
    
#Starts the game
def start() : 

    #init window
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Tris")
    draw_grid(screen)

    #init font
    pg.font.init()
    myfont = pg.font.SysFont('Comic Sans MS', 30)
    
    result = ""
    done = False
    
    #main loop
    while not done:

        #check if the game is over
        end, result =  is_ended(tris)        
        if end:
            #if the game is over displays the winner
            textsurface = myfont.render(result, False, (255, 255, 255))
            screen.blit(textsurface, (10, 10))
            pg.display.flip() 

            #wait for user's click
            con = True            
            while con:
                for ev in  pg.event.get():
                    if ev.type == QUIT:
                        pg.quit()
                    elif ev.type == MOUSEBUTTONDOWN or ev.type == KEYDOWN:
                        con = False
            
            #resetting the game on user's click
            reset()
            result = ""
            end = False 
            screen = pg.display.set_mode((WIDTH, HEIGHT))
            draw_grid(screen)
        
        #getting user's input
        for ev in  pg.event.get():
            if ev.type == QUIT:
                done = True
            elif ev.type == MOUSEBUTTONDOWN:
                handle_click(screen, ev, 'X')

    pg.quit()            

start()