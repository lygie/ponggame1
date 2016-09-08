# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [-3,random.randrange(2,4)]
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2]
paddle1_vel = [0,0]
paddle2_pos = [WIDTH-HALF_PAD_WIDTH, HEIGHT/2]
paddle2_vel = [0,0]
acc = 0
acc2 = 0
score1 = 0
score2 = 0
right = True

#if random.random() > .5:
#    right = True
#else:
#    right = False

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    if right:
        ball_vel[0] = random.randrange(1,5)
    else:
        ball_vel[0] = -random.randrange(1,5)
    
    ball_pos[0] = WIDTH/2
    ball_pos[1] = HEIGHT/2
    ball_vel[1] = -random.randrange(2,4)
    

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2
    score1 = 0
    score2 = 0# these are ints
    ball_init(right)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] - HALF_PAD_HEIGHT <= 0:
        paddle1_pos[1] = HALF_PAD_HEIGHT + 1
    elif paddle1_pos[1] + HALF_PAD_HEIGHT >= HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT - 1
    else:
        paddle1_pos[1] += paddle1_vel[1]
    if paddle2_pos[1] - HALF_PAD_HEIGHT <= 0:
        paddle2_pos[1] = HALF_PAD_HEIGHT + 1
    elif paddle2_pos[1] + HALF_PAD_HEIGHT >= HEIGHT:
        paddle2_pos[1] = HEIGHT-HALF_PAD_HEIGHT - 1    
    else:
        paddle2_pos[1] += paddle2_vel[1]  
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_polygon([[paddle1_pos[0]-HALF_PAD_WIDTH, paddle1_pos[1]-HALF_PAD_HEIGHT],
                    [paddle1_pos[0]+HALF_PAD_WIDTH, paddle1_pos[1]-HALF_PAD_HEIGHT],
                    [paddle1_pos[0]+HALF_PAD_WIDTH, paddle1_pos[1]+HALF_PAD_HEIGHT],
                    [paddle1_pos[0]-HALF_PAD_WIDTH, paddle1_pos[1]+HALF_PAD_HEIGHT]]
                     ,1,'White', 'White')
    
    c.draw_polygon([[paddle2_pos[0]-HALF_PAD_WIDTH, paddle2_pos[1]-HALF_PAD_HEIGHT],
                    [paddle2_pos[0]+HALF_PAD_WIDTH, paddle2_pos[1]-HALF_PAD_HEIGHT],
                    [paddle2_pos[0]+HALF_PAD_WIDTH, paddle2_pos[1]+HALF_PAD_HEIGHT],
                    [paddle2_pos[0]-HALF_PAD_WIDTH, paddle2_pos[1]+HALF_PAD_HEIGHT]]
                     ,1,'White', 'White')
    c.draw_circle([ball_pos[0], ball_pos[1]], BALL_RADIUS, 1, 'White', 'White')
    # update ball
   
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT and ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            ball_init(True)
            score2inc()
            #print "Score for Player 2"
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT and ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]        
        else:
            ball_init(False)
            score1inc()
            #print 'Score for Player 1'
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]        
    # draw ball and scores
    c.draw_text(str(score1), [235,50],50, "White")
    c.draw_text(str(score2), [340,50],50, "White")    
        
def score1inc():
    global score1
    score1 += 1
    return score1

def score2inc():
    global score2
    score2 += 1
    return score2

def keydown(key):
    global paddle1_vel, paddle2_vel, acc, acc2
    acc = 3
    acc2 =3
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= acc2
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += acc2
                              
    
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        acc = 0
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP["s"]:
        acc = 0
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP["up"]:
        acc2 = 0
        paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP["down"]:
        acc2 = 0
        paddle2_vel[1] = 0

def restart():
    new_game()
        
# create frame

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset_button = frame.add_button("Restart", restart)

# start frame
frame.start()
new_game()