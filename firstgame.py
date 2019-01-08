##########
# Baby's first game

# A Python game made with pygame
##########

import pygame, sys, random, time
from pygame.locals import *

# Configuration
pygame.init()

windowWidth  = 640
windowHeight = 480

windowSurface = pygame.display.set_mode(( windowWidth, windowHeight ))

fpsClock = pygame.time.Clock()
fps      = 60

pygame.display.set_caption('Baby\'s first game')

pygame.mouse.set_visible( False )
pygame.event.set_grab( True )

# Game colors
Colors = {
  'gray'     : ( 100, 100, 100 )
, 'navyBlue' : ( 60, 60, 100 )
, 'white'    : ( 255, 255, 255 )
, 'black'    : ( 0, 0, 0 )
, 'red'      : ( 255, 0, 0 )
, 'green'    : ( 0, 255, 0 )
, 'blue'     : ( 0, 0, 255 )
, 'yellow'   : ( 255, 255, 0 )
, 'orange'   : ( 255, 128, 0 )
, 'purple'   : ( 255, 0, 255 )
, 'cyan'     : ( 0, 255, 255 )
}

EnemyColors = [
  Colors['red']
, Colors['yellow']
, Colors['orange']
]

# create player actor class.  create instance.  events like mouse button alter properties
#  of that instance while the main loop is always using the same instance, but the props
#  are updated before the next pass

Player = type('Player', ( object, ), {
  'width'          : 10
, 'height'         : 50
, 'color'          : Colors['purple']
, 'startingHealth' : 100
, 'health'         : 100
})

Gamefield = type('Gamefeld', ( object, ), {
  'defaultBackfieldWidth' : 50
, 'backfieldWidth'        : 50
, 'bgColor'               : Colors['navyBlue']
, 'defaultEndfieldWidth'  : 50
, 'endfieldWidth'         : 50
})

Session = type('Session', ( object, ), {
  'circularMode'            : True
, 'defaultCircularOffset'   : 0.1
, 'circularOffset'          : 0.1
, 'circularOffsetInvert'    : False
, 'mouseX'                  : 0
, 'mouseY'                  : 0
, 'maxEnemiesOnScreen'      : 5
, 'defaultEnemySpeedOffset' : 0.5
, 'enemySpeedOffset'        : 0.5
, 'enemySpawnDelayOffset'   : 0.5
, 'currentEnemies'          : 0
, 'timeOfLastEnemySpawn'    : 0
})

Enemy = type('Enemy', ( object, ), {
  'width'          : 10
, 'height'         : 10
, 'color'          : random.choice( EnemyColors )
, 'startingHealth' : 100
, 'health'         : 100
, 'startingPos'    : (0, 0)
, 'curPos'         : (0, 0)
, 'speed'          : 1
, 'spawnDelay'     : 0
})

# Main game function
def main():
  # Init Session, Gamefield, and Player objects
  session   = Session()
  gamefield = Gamefield()
  player    = Player()
  enemies   = []

  # Gamefield defaults
  gamefield.defaultGamefieldWidth = windowWidth - ( gamefield.defaultBackfieldWidth + gamefield.defaultEndfieldWidth )
  gamefield.gamefieldWidth        = gamefield.defaultGamefieldWidth
  gamefield.startX                = gamefield.defaultBackfieldWidth
  gamefield.endX                  = gamefield.startX + gamefield.defaultGamefieldWidth

  # add function that creates enemy waves and spawns one at a time with a small delay
  # 1. create random batch of enemies, 2. draw enemies when their queue position comes up?

  for enemy in range( 1, session.maxEnemiesOnScreen ):
    enemies.append( Enemy() )

  # Create enemies
  for enemy in enemies:
    enemy.color       = random.choice( EnemyColors )

    if enemy.color == Colors['yellow']:
      enemy.speed = random.randint(1, 3)
    elif enemy.color == Colors['orange']:
      enemy.speed = random.randint(4, 7)
    elif enemy.color == Colors['red']:
      enemy.speed = random.randint(8, 11)

    randomX = random.randint(( gamefield.endX + enemy.width ), ( windowWidth - enemy.width ))
    randomY = random.randint( enemy.height, ( windowHeight - enemy.height ))
    enemy.startingPos = ( randomX, randomY )
    enemy.curPos      = enemy.startingPos

    enemy.spawnDelay = random.randint(0, 5)


  # Constants and other inits
  cursorOffset = player.height / 2
  backfieldIncrease = 0


  # Main game loop
  runGame = True
  while runGame:
    ##########
    # Event loop
    ##########
    for event in pygame.event.get():

      if event.type == KEYUP:
        print event

      # Quit the game
      if event.type == QUIT or ( event.type == KEYUP and event.key == K_ESCAPE ):
        runGame = False

      ##########
      # Circular mode
      ##########
      # Toggle circular movement
      if event.type == KEYUP and event.key == 287:
        if session.circularMode == False:
          session.circularMode = True
          print('circularMode enabled') #  these should be in-game text alerts
        elif session.circularMode == True:
          session.circularMode = False
          print('circularMode disabled') # these should be in-game text alerts

      # Toggle circular offset inversion
      if event.type == KEYUP and event.key == 288:
        if session.circularOffsetInvert == False:
          session.circularOffsetInvert = True
          print('circularOffset inverted') # these should be in-game text alerts
        elif session.circularOffsetInvert == True:
          session.circularOffsetInvert = False
          print('circularOffset normal') # these should be in-game text alerts

      # Inc/dec circularOffset
      if event.type == KEYUP and event.key == 61:
        session.circularOffset += 0.1
        print session.circularOffset
      elif event.type == KEYUP and event.key == 45:
        session.circularOffset -= 0.1
        print session.circularOffset
      elif event.type == KEYUP and event.key == 48:
        session.circularOffset = session.defaultCircularOffset
        print session.circularOffset


      ##########
      # Mouse events
      ##########
      # Mouse movement
      if event.type == MOUSEMOTION:
        session.mouseX, session.mouseY = event.pos

      # Mouse clicks and scrolls
      if event.type == MOUSEBUTTONUP:
        if event.button == 1 or event.button == 5:
          print 'mouse one'
        if event.button == 3 or event.button == 4:
          print 'mouse two'

    ##########
    # Game logic
    ##########

    # Fill background
    windowSurface.fill( gamefield.bgColor )

    # Adjust backfieldWidth for circularMode
    if session.circularMode:
      for val in range( 0, windowHeight ):
        # Mouse in upper half
        if session.mouseY == val and val <= ( windowHeight / 2 ):
          backfieldIncrease = (( windowHeight / 2 ) - val ) * session.circularOffset
          break
        # Mouse in lower half
        elif session.mouseY == val and val >= ( windowHeight / 2 ):
          backfieldIncrease = ( val - ( windowHeight / 2 )) * session.circularOffset
          break
        
        # Set the backfield
        if session.circularOffsetInvert:
          # Inverted increase
          gamefield.backfieldWidth = gamefield.defaultBackfieldWidth - backfieldIncrease
        else:
          gamefield.backfieldWidth = gamefield.defaultBackfieldWidth + backfieldIncrease

    else: 
      gamefield.backfieldWidth = gamefield.defaultBackfieldWidth


    # Check for empty enemies
    # if len( enemies ) <= 1:
      # spawn enemies


    # Enemy movement
    for enemy in enemies:
      # also add what happens when enemy collides with player
      if enemy.curPos[0] <= gamefield.backfieldWidth:
        # Player takes a hit, enemy dies
        enemies.remove( enemy )
      else:
        # Adjust X position
        enemyX = enemy.curPos[0] - ( enemy.speed * session.enemySpeedOffset )
        enemy.curPos = ( enemyX, enemy.curPos[1] )


    ##########
    # Drawerings by Simon
    ##########

    # Draw the player
    # drawPlayerRectangle( gamefield.backfieldWidth, ( session.mouseY - cursorOffset ), player.width, player.height )
    drawPlayer(( gamefield.backfieldWidth, ( session.mouseY - cursorOffset )), player )

    # Draw enemies
    for enemy in enemies:
      # If time between now and last spawn is >= enemy's spawn time, draw that enemy
      # if ( pygame.time.get_ticks() - session.timeOfLastEnemySpawn ) >= ( enemy.spawnDelay * 1000 ):
      drawEnemy( enemy.curPos, enemy )
        # session.timeOfLastEnemySpawn = pygame.time.get_ticks()


    # Update display
    Tick()

def Tick():
  pygame.display.update()
  fpsClock.tick( fps )

# Draws player rectangle
def drawPlayerRectangle( top = 0, left = 0, width = 10, height = 50 ):
  pygame.draw.rect( windowSurface, Colors['white'], ( top, left, width, height ))

def drawPlayer( pos, player ):
  pygame.draw.rect( windowSurface, player.color, ( pos[0], pos[1], player.width, player.height ))

def drawEnemy( pos, enemy ):
  pygame.draw.rect( windowSurface, enemy.color, ( pos[0], pos[1], enemy.width, enemy.height ))


# Start
if __name__ == '__main__':
  main()

# Quit
pygame.quit()
sys.exit()