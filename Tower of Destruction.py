#This is a platformer game where you have to escape the lava by jumping on platforms. Currently only 1600 platforms are supported as opposed to it infinitely generating, and some platforms may be seemingly impossible to cross.

from tkinter import *
from time import *
from random import *

root = Tk()
screen = Canvas(root, width=600, height=600, background="grey")

def setInitialValues():
  global score, xMan, yMan, xSpeed, ySpeed, falling, yLava, movingLeft, movingRight, movingUp 
  global xPlatform, yPlatform, numPlatforms, currentTime, startTime, introScreen, lost
  score = 0
  xMan = 50
  yMan = 450 #where character starts
  xSpeed = 0
  ySpeed = 0
  yLava = 1200 #lava starts at 1200
  movingLeft = 0 #0 and 1 are used as booleans
  movingRight = 0
  movingUp = 0
  falling = 1 #player starts falling
  numPlatforms = 1600 #1600 platforms made
  currentTime = time()
  startTime = time() #these will be used for the jump/gravity function, but are defined now just in case
  introScreen = 1
  lost = 0
  createPlatform() #creates platforms

def drawIntro():
  global intro, title, castle, text
  title = screen.create_text(300, 150, text="Tower of Destruction", font="Times 30", fill="red") 
  intro = screen.create_text(300, 200, text="Use the arrow keys or WASD to move around, hold up to jump higher!", font="Times 12", fill="red")
  text = screen.create_text(300, 225, text="Click to start!", font= "Times 11", fill="red")
  castle = screen.create_polygon(175, 275, 225, 275, 225, 325, 275, 325, 275, 275, 325, 275, 325, 325, 375, 325, 375, 275, 425, 275, 425, 550, 175, 550, 175, 275, outline="black", fill="")

def drawBackground():
  global row, colum, yRow, yColumn
  row = []
  colum = []
  yRow = -30
  for i in range (21):
    row.append(screen.create_line(0, yRow, 600, yRow))
    yRow += 30
    for j in range (20):
      if yRow % 60 == 30:
        xColumn = j * 60 - 30
      else:
        xColumn = j * 60
      colum.append(screen.create_line(xColumn, yRow, xColumn, yRow + 30))

def loseGame(): #if player loses
  global loseScreen, score
  text = "You lost! Your score was " + str(score) + ". Click to play again!"
  loseScreen = screen.create_text(300, 300, text=text, font="Times 12", fill="red")

def drawObjects(): #draws the character, platforms, background, and lava
  global xMan, yMan, yLava, head, body, lava
  drawBackground()
  updatePlatforms()
  head = screen.create_oval(xMan - 25, yMan, xMan + 25, yMan + 50, fill="red")
  body = screen.create_rectangle(xMan - 25, yMan + 25, xMan + 25, yMan + 100, fill="green")
  lava = screen.create_rectangle(0, yLava, 800, 1200, fill="orange", outline="orange")

def createPlatform():
  global xPlatform, yPlatform, platformHeight, platformWidth, platformDrawing, numPlatforms
  platformHeight = [5]
  platformWidth = [50]
  xPlatform = [50]
  yPlatform = [575]
  platformDrawing = [0] #first platform will always be at the same place

  for i in range (numPlatforms):
    platformHeight.append(5)
    platformWidth.append(randint(50, 100))
    platformDrawing.append(0)
    xPlatform.append(randint(xPlatform[i - 1] - 75, xPlatform[i - 1] + 75)) #the next platform should always be within 75 pixels of the last one in terms of x range
    if xPlatform[i] < 0:
      xPlatform[i] = 600 - xPlatform[i]
    elif xPlatform[i] > 600:
      xPlatform[i] -= 600  #if the platform is off screen, bring it back on screen on the other side; character can also loop around to take advantage of this
    yPlatform.append(randint(yPlatform[i] - 80, yPlatform[i] - 30)) #the next platform should always be between 30 and 80 pixels above the previous one


def updatePlatforms():
  global platformDrawing, xPlatform, platformWidth, yPlatform, platformHeights, numPlatforms
  for i in range (numPlatforms + 1):
    platformDrawing[i] = screen.create_rectangle(xPlatform[i]-(1/2)*platformWidth[i], yPlatform[i], xPlatform[i]+(1/2)*platformWidth[i], yPlatform[i]+platformHeight[i], fill="green") #draws the platforms

def updateObjects():
  global xMan, yMan, xSpeed, ySpeed, score, yLava, movingLeft, movingRight, movingUp, falling
  global currentTime, startTime, numPlatforms, platformWidth, xPlatform, yPlatform, lost
  if movingLeft == 1: #moving left
    xSpeed = -5
  else:
    xSpeed = 0
  if movingRight == 1: #moving right
    xSpeed = 5
  currentTime = time()
  if currentTime - startTime > 2: #if the jump button has been held for too long, automatically stop the jump process
    falling = 1
    movingUp = 0
  if movingUp == 1:
    ySpeed = -5
    falling = 0
  elif yMan < 500:
    falling = 1
  else:
    lost = 1 #if yMan under 500, lose
  if falling == 1:
    ySpeed = 5
  if yLava > 1200:
    yLava = 1200 #yLava never goes under y=1200
  if yMan + 100 > yLava: #if character touches lava, lose
    lost = 1

  xMan += xSpeed
  yMan += ySpeed
  yLava -= 3 #Lava raises at a constant rate of 3px/s
  if 450 - yMan > score:
    score = 450 - yMan
  scrolldown()

def scrolldown():
  global yMan, yLava, yPlatform, score, yRow, ydifference
  if yMan < 200: #if the character is above a specific line, keep it at that line and scroll everything else down to make it seem like the character is moving up
    ydifference = 200 - yMan
    yMan = 200
    yLava += ydifference
    score += ydifference
    yRow += ydifference
    for i in range (len(yPlatform)):
      yPlatform[i] += ydifference

def checkForCollisions():
  global yMan, xMan, yPlatform, xPlatform, xSpeed, ySpeed, falling 
  global numPlatforms, platformWidth
  if xMan < 0:
    xMan += 600
  if xMan > 600:
    xMan -= 600 #some code for character looping around
  if falling == 1:
    for i in range(numPlatforms):
      if xPlatform[i] - platformWidth[i]  < xMan < xPlatform[i] + platformWidth[i]: #if xCharacter is between the platform's boundaries and is right above one
        if yPlatform[i] < yMan + 100 < yPlatform[i] + 6:  
          ySpeed = 0
          falling = 0
          yMan = yPlatform[i] - 100 #collision detection
        else:
          falling = 1 

def mouseClickHandler( event ):
  global introScreen, lost
  if introScreen == 1:
    introScreen = 0
  if lost == 1:
    lost = 0
    introScreen = 1

def keyDownHandler( event ): #when key is pressed
  global movingLeft, movingRight, movingUp, falling, startTime

  if event.keysym == "Left" or event.keysym == "A" or event.keysym == "a":
    movingLeft = 1

  if event.keysym == "Right" or event.keysym == "D" or event.keysym == "d":
    movingRight = 1

  if event.keysym == "Up" or event.keysym == "W" or event.keysym == "w":
    if ySpeed == 0: #makes sure you can only jump when you are standing still
      movingUp = 1
      falling = 0
      startTime = time() #starts a timer when the jump button is pressed
    else:
      pass

def keyUpHandler( event ): #if the key is released
  global movingLeft, movingRight, movingUp, falling
  if event.keysym == "Left" or event.keysym == "A" or event.keysym == "a":
    movingLeft = 0

  if event.keysym == "Right" or event.keysym == "D" or event.keysym == "d":
    movingRight = 0

  if event.keysym == "Up" or event.keysym == "W" or event.keysym == "w":
    movingUp = 0
    falling = 1
    

def runGame():

  setInitialValues() 

  while True:
    if introScreen == 1:
      setInitialValues() #initial values are all reset
      drawIntro()
      screen.update()
      sleep(0.03)
      screen.delete(intro, title, castle, text)

    elif lost == 1:
      loseGame()
      screen.update()
      sleep(0.03)
      screen.delete(loseScreen)

    else:
      drawObjects()

      screen.update()
      sleep(0.03)
      screen.delete(head, body, lava, row, colum)
      for i in range(len(platformDrawing)):
        screen.delete(platformDrawing[i])
      for i in range(len(row)):
        screen.delete(row[i])
      for i in range(len(colum)):
        screen.delete(colum[i])

      updateObjects()  
      checkForCollisions()

#Call the runGame function
root.after( 0, runGame )

#Connecting user inputs to functions
screen.bind( "<Button-1>", mouseClickHandler )
screen.bind( "<Key>", keyDownHandler )

#If you wanted to detect a key being released
screen.bind( "<KeyRelease>", keyUpHandler )

screen.pack()
screen.focus_set()
root.mainloop()