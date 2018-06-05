#import pygame
import turtle
import random
import winsound

#screen setter
screen = turtle.Screen()
screen.setup(678,3000,0,0)
screen.bgcolor("blue")
screen.title("Escape")
#screen.bgpic("...")

#game music
winsound.PlaySound("escape_music.wav", winsound.SND_ASYNC)

#Register shapes for characters
#turtle.register_shape()

#Walls
wall1 = turtle.Turtle()
wall1.shape("square")
wall1.penup()
wall1.shapesize(100)
wall1.setposition(-1070,0)

wall2 = turtle.Turtle()
wall2.shape("square")
wall2.penup()
wall2.speed(0)
wall2.shapesize(100)
wall2.setposition(1070,0)

#player turtle
player = turtle.Turtle()
player.color("red")
player.shape("circle")
player.penup()
#Test at (0,200)
player.setposition(0,0)

#player hp
playerhp = 4
#ACTUAL HP
php = 3

pspeed = 15

#Draw player health bar
playerhp_pen = turtle.Turtle()
playerhp_pen.speed(0)
playerhp_pen.color("red")
playerhp_pen.shape("square")
playerhp_pen.penup()
playerhp_pen.shapesize(1,playerhp)
playerhp_pen.setposition(-290,350)
#boss hp txt
playerhp_pen1 = turtle.Turtle()
playerhp_pen1.speed(0)
playerhp_pen1.color("white")
playerhp_pen1.penup()
playerhp_pen1.setposition(-290,340)
playerhpstr = "Player HP: %s" %php
playerhp_pen1.write(playerhpstr, False, "left",("Arial", 8))
playerhp_pen1.ht()

#Rising pit turtle
rpit = turtle.Turtle()
rpit.color("purple")
rpit.shape("circle")
rpit.penup()
rpit.speed(0)
rpit.shapesize(40)
#Test at y = -200 ORIG -500
rpit.setposition(0,-500)

rpitspeed = 3

#Anouncement
alert1 = turtle.Turtle()
alert1.speed(0)
alert1.color("white")
alert1.penup()
alert1.setposition(0,250)
txt = "Don't get caught by the rising pit!!! Get to safety above this txt!"
alert1.write(txt, False, "center",("Arial", 12))
alert1.ht()

#Falling enemies        
enemies = turtle.Turtle()
enemies.penup()
enemies.color("yellow")
enemies.shape("triangle")
enemies.speed(0)
enemies.setheading(-90)
enemies.shapesize(1.5,1.5)



enem_speed = 10


#Spawn objects randomly from certain position
def spawn_enemy():
    global player 
    global enemies
    
    x = random.randint(-60, 60)
    y = player.ycor() + 500 
    enemies.setposition(x,y)
        
    return enemies,enem_speed

#Move player up, down, left, and right
def move_up():
    y = player.ycor()
    y+=pspeed
    if y>400:   
        y = 400
    player.sety(y)
    
def move_down():
    y = player.ycor()
    y-=pspeed
    player.sety(y)
    
def move_right():
    x = player.xcor()
    x+=pspeed
    if x>60:
        x = 60
    player.setx(x)

def move_left():
    x = player.xcor()
    x-=pspeed
    if x<-60:
        x = -60
    player.setx(x)  
    
#Check for collisions
def collision(t1, t2):
    dist = ((t1.xcor()-t2.xcor())**2+(t1.ycor()-t2.ycor())**2)**(1/2)
    if dist<10:
        return True
    else:
        return False

#player and enemies collision
def scollision(t1, t2):
    dist = ((t1.xcor()-t2.xcor())**2+(t1.ycor()-t2.ycor())**2)**(1/2)
    if dist<15:
        return True
    else:
        return False
    
#pbull and boss thunder bullets with player collision   
def bcollision(t1, t2):
    dist = ((t1.xcor()-t2.xcor())**2+(t1.ycor()-t2.ycor())**2)**(1/2)
    if dist<60:
        return True
    else:
        return False

#TEST for thunder bullets with player collision 
def tcollision(t1, t2):
    dist = ((t1.xcor()-t2.xcor())**2+(t1.ycor()-t2.ycor())**2)**(1/2)
    if dist<27:
        return True
    else:
        return False

    
def game_over():
    screen.reset()
    screen.bgcolor("black")
    text = turtle.Turtle()
    text.speed(0)
    text.color("white")
    text.penup()
    text.write("GAME OVER", True, "center",("Times New Roman", 20))
    text.ht()
    
def you_won():
    screen.reset()
    screen.bgcolor("black")
    text = turtle.Turtle()
    text.speed(0)
    text.pencolor("white")
    text.penup()
    text.write("Congratulations, You Won!", True, "center",("Times New Roman", 20))
    text.ht()
    

#Keyboard binding
turtle.listen()
turtle.onkey(move_up,"Up")
turtle.onkey(move_down, "Down")
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")

#player caught by pit or hit by falling enemies
caught = False

#Game loop
spawn_enemy()
while caught==False and playerhp>1:
    #rising pit
    y = rpit.ycor()
    y += rpitspeed
    rpit.sety(y)
    
    #falling enemies
    y = enemies.ycor()
    y -= enem_speed
    enemies.sety(y)    

    #pit catches up to player after a certain position
    if rpit.ycor()+390 >= player.ycor()>=250:
        caught = True
        #Set up what comes after
        enemies.hideturtle()
        rpit.setposition(0,0)
        player.setposition(0,0)
    #player catches up to player b4 a certain position    
    elif rpit.ycor()+390 >= player.ycor()<250:
        caught = True
        playerhp = 1

    #enemies hits player
    if collision(player, enemies):
        #player loses hp
        playerhp-=1
        php-=1
        #update playerhp bar and txt
        playerhp_pen.clear()
        playerhp_pen1.clear()
        playerhpstr = "Player HP: %s" %php
        playerhp_pen.shapesize(1,playerhp)
        playerhp_pen1.write(playerhpstr, False, "left",("Arial", 8))
               
    elif enemies.ycor() <= player.ycor()-50:
        spawn_enemy()

alert1.clear()    
    
if playerhp==1:
    print("Game Over")
    winsound.PlaySound(None, winsound.SND_ASYNC)
    game_over()
#list of enemies and bullets
enemies_lst = []
bullets_lst = []

#y position of enemies
y = 200

if rpit.pos()==(0,0) and player.pos()==(0,0) and playerhp>1:
    #Anouncement
    alert = turtle.Turtle()
    alert.speed(0)
    alert.color("white")
    alert.penup()
    alert.setposition(0,250)
    txt = "You found a gun with a reusable bullet in the pit. GET RID OF THE ENEMY and ESCAPE!"
    alert.write(txt, False, "center",("Arial", 12))
    alert.ht()
    
    #Player bullets (2)
    bull1 = turtle.Turtle()
    bull1.color("pink")
    bull1.shape("circle")
    bull1.penup()
    bull1.speed(0)
    bull1.shapesize(1,1)
    bull1.ht()

    bull1state = "ready"
    #bulletspeed
    pbullspeed = 8
    p_bossbullspeed = 20
    bull1direction = "left"
       
    #Player movement restrictions edited 
    def move_up_edit():
        y = player.ycor()
        y+=pspeed
        if y>170:   
            y = 170
        player.sety(y)
    
    def move_down_edit():
        y = player.ycor()
        y-=pspeed
        if y<-150:
            y = -150
        player.sety(y)
    
    def move_right_edit():
        x = player.xcor()
        x+=pspeed
        if x>200:
            x = 200
        player.setx(x)
    
    def move_left_edit():
        x = player.xcor()
        x-=pspeed
        if x<-200:
            x = -200
        player.setx(x)
    
    ## of enemies
    #EDIT BCK TO 7
    enemycnt = 7
    #enemies in pit and bullets
    for i in range(7):
        enemies_lst.append((turtle.Turtle(),turtle.Turtle()))
        #tuple for left and right bullets
        bullets_lst.append((turtle.Turtle(),turtle.Turtle()))
        
    for enemies in enemies_lst:
        enemies[0].color("yellow")
        enemies[0].shape("triangle")
        enemies[0].penup()
        enemies[0].speed(0)
        enemies[0].setheading(0)
        enemies[0].shapesize(1.5,1.5)
            
        enemies[1].color("yellow")
        enemies[1].shape("triangle")
        enemies[1].penup()
        enemies[1].speed(0)
        enemies[1].setheading(180)
        enemies[1].shapesize(1.5,1.5)
        
        y-=50
        #positioning the enemy to the left   
        #enemies[0].setheading(0)
        enemies[0].setposition(-200,y)
        
        #positioning the enemy to the right         
        #enemies[1].setheading(180)
        enemies[1].setposition(200,y)

    for bullet in bullets_lst:
        #enemy bullets
        bullet[0].color("orange")
        bullet[0].shape("circle")
        bullet[0].penup()
        bullet[0].speed(0)
        #bullet[0].setheading(0)
        bullet[0].shapesize(0.5,2)
        bullet[0].hideturtle()
        
        bullet[1].color("orange")
        bullet[1].shape("circle")
        bullet[1].penup()
        bullet[1].speed(0)
        #bullet[1].setheading(180)
        bullet[1].shapesize(0.5,2)
        bullet[1].hideturtle()
    

    #bulletspeed
    bull_speed = 50
    bull_state = "ready"

    #bullet to shoot
    
    #enemy fire bullet
    def ready_bullets():
        global bull_state
        y = 200
        
        if bull_state == "ready":
            bull_state = "shoot"
            for bullet in bullets_lst:
                #move bullet in front of enemy
                y-=50
                #move the bullets from the left   
                bullet[0].setheading(0)
                bullet[0].setposition(-160,y)
                
                #move the bullets from the right         
                bullet[1].setheading(180)
                bullet[1].setposition(160,y)
                
                bullet[0].ht()
                bullet[1].ht()
      
    def fire_pbullets():
        global bull1state
        global bull1direction

        if player.xcor()>0:
            bull1direction = "right"
            y = player.ycor()
            x = player.xcor()+10
        elif player.xcor()<0:
            bull1direction = "left"
            y = player.ycor()
            x = player.xcor()-10     
        #checking if bullet is ready
        if bull1state=="ready":
            bull1state = "shoot"
            bull1.setposition(x,y)
            bull1.st()


    #Edited keyboard binding
    turtle.onkey(move_up_edit, "Up")
    turtle.onkey(move_down_edit, "Down")
    turtle.onkey(move_left_edit, "Left")
    turtle.onkey(move_right_edit, "Right")
    turtle.onkey(fire_pbullets, "space")
    
    alert.clear()
    #Second main Game loop
    caught2 = False
    
    ready_bullets()
    while caught2==False and enemycnt>0:
        if playerhp==1:
            break
    
        if bull1state=="shoot":
                if bull1direction=="right":
                    x = bull1.xcor()
                    x+=pbullspeed
                    bull1.setx(x)
                
                if bull1.xcor()>200:
                    bull1.ht()
                    bull1state = "ready"
                    
                if bull1direction=="left":
                    x = bull1.xcor()
                    x-=pbullspeed
                    bull1.setx(x)
            
                if bull1.xcor()<-200:
                    bull1.ht()
                    bull1state = "ready"

        # if player touches enemies
        for enemies in enemies_lst:
            if scollision(player,enemies[0]) or scollision(player, enemies[1]):
                #player loses hp
                playerhp-=1
                php-=1
                #update playerhp bar and txt
                playerhp_pen.clear()
                playerhp_pen1.clear()
                playerhpstr = "Player HP: %s" %php
                playerhp_pen.shapesize(1,playerhp)
                playerhp_pen1.write(playerhpstr, False, "left",("Arial", 8))
                if playerhp==1:
                    break

        #moving enemy bullets        
        if bull_state =="shoot":
            for bullet in bullets_lst:
                bullet[0].st()
                bullet[1].st()
                for i in range(7):
                    l = bullet[0].xcor()
                    r = bullet[1].xcor()
                    
                    l+=bull_speed
                    r-=bull_speed
                    
                    bullet[0].setx(l)
                    bullet[1].setx(r)
                    
                    #if bullets hit player
                    if scollision(player,bullet[0]) or scollision(player,bullet[1]):
                       #player loses hp
                        playerhp-=1
                        php-=1
                        #update playerhp bar and txt
                        playerhp_pen.clear()
                        playerhp_pen1.clear()
                        playerhpstr = "Player HP: %s" %php
                        playerhp_pen.shapesize(1,playerhp)
                        playerhp_pen1.write(playerhpstr, False, "left",("Arial", 8))
                        if playerhp==1:
                            break
                    if bull1state=="shoot":
                        if bull1direction=="right":
                            x = bull1.xcor()
                            x+=pbullspeed
                            bull1.setx(x)
                    
                        if bull1.xcor()>200:
                            bull1.ht()
                            bull1state = "ready"
                            
                        if bull1direction=="left":
                            x = bull1.xcor()
                            x-=pbullspeed
                            bull1.setx(x)
                            
                        if bull1.xcor()<-200:
                            bull1.ht()
                            bull1state = "ready"
                        
                    for enemies in enemies_lst:
                        if bull1state=="shoot":
                            if bull1direction=="right":
                                x = bull1.xcor()
                                x+=pbullspeed
                                bull1.setx(x)
                        
                            if bull1.xcor()>200:
                                bull1.ht()
                                bull1state = "ready"
                                
                            if bull1direction=="left":
                                x = bull1.xcor()
                                x-=pbullspeed
                                bull1.setx(x)
                                
                            if bull1.xcor()<-200:
                                bull1.ht()
                                bull1state = "ready"
                                
                        #cheking if player bullets hit enemies    
                        if scollision(enemies[0],bull1) or scollision(enemies[1],bull1):
                            bull1.ht()
                            bull1.setposition(player.xcor(),player.ycor())
                            enemies[0].ht()
                            enemies[1].ht()
                            enemycnt-=1
                            bull1state = "ready"
                            
                        
                bullet[0].ht()
                bullet[1].ht()
        if caught2!=True:
            bull_state = "ready"
            ready_bullets()
            
    if playerhp==1:
        print("Game Over")
        game_over()

    if enemycnt==0:
        #set player back in position
        player.setposition(0,-30)
        #Final boss
        boss = turtle.Turtle()
        boss.color("gray")
        boss.shape("triangle")
        boss.penup()
        boss.speed(0)
        boss.setheading(-90)
        boss.setposition(0,600)
        boss.shapesize(10,10)
        
        bosspeed = 11
        #boss hp
        bosshp = 6
        #ACTUAL BOSS HP
        bhp = 5
        
        #Draw player health bar
        bosshp_pen = turtle.Turtle()
        bosshp_pen.speed(0)
        bosshp_pen.color("gray")
        bosshp_pen.shape("square")
        bosshp_pen.penup()
        bosshp_pen.shapesize(1,bosshp)
        bosshp_pen.setposition(-290,400)
        #boss hp txt
        bosshp_pen1 = turtle.Turtle()
        bosshp_pen1.speed(0)
        bosshp_pen1.color("white")
        bosshp_pen1.penup()
        bosshp_pen1.setposition(-290,390)
        bosshpstr = "Boss HP: %s" %bosshp
        bosshp_pen1.write(bosshpstr, False, "left",("Arial", 8))
        bosshp_pen1.ht()
        
        #boss thunder bullets
        #left bullet
        thunder = (turtle.Turtle(),turtle.Turtle())
        thunder[0].color("lightgreen")
        thunder[0].shape("triangle")
        thunder[0].penup()
        thunder[0].speed(0)
        thunder[0].setheading(-90)
        thunder[0].shapesize(2,4)
        thunder[0].ht()
        #right bullet
        thunder[1].color("lightgreen")
        thunder[1].shape("triangle")
        thunder[1].penup()
        thunder[1].speed(0)
        thunder[1].setheading(-90)
        thunder[1].shapesize(2,4)
        thunder[1].ht()
        #state of thunder bullets
        thunderstate = "ready"
        thunderspeed = 20
        
        #left minbullet
        minthunder = (turtle.Turtle(),turtle.Turtle())
        minthunder[0].color("lightblue")
        minthunder[0].shape("circle")
        minthunder[0].penup()
        minthunder[0].speed(0)
        minthunder[0].setheading(-90)
        minthunder[0].shapesize(2,4)
        minthunder[0].ht()
        #right minbullet
        minthunder[1].color("lightblue")
        minthunder[1].shape("circle")
        minthunder[1].penup()
        minthunder[1].speed(0)
        minthunder[1].setheading(-90)
        minthunder[1].shapesize(2,4)
        minthunder[1].ht()
        
        def move_down_edit2():
            y = player.ycor()
            y-=pspeed
            if y<-30:
                y = -30
            player.sety(y)
            
        #only fire bullets at boss above from a certain distance
        def fire_pbullets2():
            global bull1state
            y = player.ycor()+10
            x = player.xcor()
            
            #checking if bullet is ready
            if bull1state=="ready":
                bull1state = "shoot"
                bull1.setposition(x,y)
                bull1.st()
           
           
        def fire_boss_bullets():
            global thunderstate
            #left bullet position
            x1 = boss.xcor()-50
            y1 = boss.ycor()-70
            #right bullet position
            x2 = boss.xcor()+50
            y2 = boss.ycor()-50
            
            thunder[0].setposition(x1,y1)
            thunder[1].setposition(x2,y2)
            
            minthunder[0].setposition(x1-80,y1-20)
            minthunder[1].setposition(x2+80,y2+20)
            
            thunder[0].st()
            thunder[1].st()
            minthunder[0].st()
            minthunder[1].st()
            
            thunderstate = "shoot"
      
        #Edited keyboard binding
        turtle.onkey(move_down_edit2, "Down")
        turtle.onkey(fire_pbullets, "space")
        
        #boss entrance
        while boss.ycor()>300:
            #move boss down
            y = boss.ycor()
            y-=bosspeed
            boss.sety(y)
        
        p1 = player
        th = thunder
        minth = minthunder
        fire_boss_bullets()
        #third main game loop
        while bosshp>1 and playerhp>1:
            #move boss
            x = boss.xcor()
            x+=bosspeed
            boss.setx(x)
            
            if thunderstate=="shoot":
                y = minth[0].ycor()
                y-=thunderspeed
                minth[0].sety(y)
                
                y = th[0].ycor()
                y-=thunderspeed
                th[0].sety(y)
                
                y = th[1].ycor()
                y-=thunderspeed
                th[1].sety(y)
                
                y = minth[1].ycor()
                y-=thunderspeed
                minth[1].sety(y)
                
            
            #move boss left and right
            if boss.xcor()>210:
                bosspeed *= -1
            
            if boss.xcor()<-210:
                bosspeed *= -1
            
            #pbullets hit boss
            if bcollision(boss,bull1):
                bull1.ht()
                bull1.setposition(player.xcor(),player.ycor())
                #player loses hp
                bosshp-=1
                bhp-=1
                #update playerhp bar and txt
                bosshp_pen.clear()
                bosshp_pen1.clear()
                bosshpstr = "Boss HP: %s" %bhp
                bosshp_pen.shapesize(1,bosshp)
                bosshp_pen1.write(bosshpstr, False, "left",("Arial", 8))
                bull1state = "ready"
            
            if bcollision(boss,p1) or tcollision(th[0],p1) or tcollision(th[1],p1) or tcollision(minth[0],p1) or tcollision(minth[1],p1):
                #player loses hp
                playerhp-=1
                php-=1
                #update playerhp bar and txt
                playerhp_pen.clear()
                playerhp_pen1.clear()
                playerhpstr = "Player HP: %s" %php
                playerhp_pen.shapesize(1,playerhp)
                playerhp_pen1.write(playerhpstr, False, "left",("Arial", 8))
                
                minth[0].ht()
                th[0].ht()
                th[1].ht()
                minth[1].ht()
                thunderstate = "shoot"
                
            if minth[0].ycor()<-25:
                minth[0].ht()
            if th[0].ycor()<-25:
                th[0].ht()
            if th[1].ycor()<-25:
                th[1].ht()
            if minth[1].ycor()<-25:
                minth[1].ht()
                thunderstate="ready"
            
            #mvoe pbullet
            if bull1state=="shoot":
                y = bull1.ycor()
                y+=p_bossbullspeed
                bull1.sety(y)
                
            #if bullet goes way pass boss
            if bull1.ycor()>400:
                bull1.ht()
                bull1state = "ready"
                                
            #check if thunderbullets are ready
            if thunderstate=="ready":
                fire_boss_bullets()
        
        if bosshp==1:
            print("Congratulations, You Won!")
            winsound.PlaySound(None, winsound.SND_ASYNC)
            you_won()
            
if playerhp==1:
    print("Game Over")
    winsound.PlaySound(None, winsound.SND_ASYNC)
    game_over()
 
turtle.done()
