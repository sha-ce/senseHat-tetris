#必要なライブラリをimport
import time
import sense_hat
import numpy as np
import sys

sense = sense_hat.SenseHat()
sense.clear()

#ジョイスティック設定
left_key   = sense_hat.DIRECTION_LEFT
right_key  = sense_hat.DIRECTION_RIGHT
up_key     = sense_hat.DIRECTION_UP
down_key   = sense_hat.DIRECTION_DOWN
middle_key = sense_hat.DIRECTION_MIDDLE
pressed    = sense_hat.ACTION_PRESSED
released   = sense_hat.ACTION_RELEASED

#画面の回転
sense.set_rotation(90)
left_key  = sense_hat.DIRECTION_UP
right_key = sense_hat.DIRECTION_DOWN
up_key    = sense_hat.DIRECTION_RIGHT
down_key  = sense_hat.DIRECTION_LEFT


#フィールドサイズ
playfieldSize = 10
playfield = np.zeros((playfieldSize, playfieldSize))

#ゲームスピード
gameSpeed = 0.8

#main関数での変数
lft = 0.0
timeCounter = 0.0
score = 0
interval = gameSpeed
gameOver = False

#LEDマトリックスの外に境界線を作る
for i in range(0, playfieldSize):
    #playfield[i][0] = 1
    playfield[i][playfieldSize-1] = 1
    playfield[0][i] = 1
    playfield[playfieldSize-1][i] = 1
#
#playfield
#       0  1  2  3  4  5  6  7  8  9
#
#   0   1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#   1   1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#   2   1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#   3   1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#   4   1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#   5   1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#   6   1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#   7   1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#   8   1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#   9   1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#


#テトリスの色を定義
tetroColor = {
    0:(0, 0, 0),
    1:(0, 255, 255),   #1-水
    2:(0, 0, 255),     #2-青
    3:(255, 0, 255),   #3-紫
    4:(255, 255, 0),   #4-黄
    5:(255, 0, 0),     #5-赤
    6:(0, 255, 0),     #6-緑
    7:(255, 255, 255)  #7-白
}

#テトリミノの形を定義
tetroType = np.array([
    [0x38, 0x92, 0x38, 0x92],     #1-I
    [0x93, 0x78, 0x192, 0x1E0],   #2-L
    [0x96, 0x1C8, 0xD2, 0x138],   #3-J
    [0x9A, 0xB8, 0xB2, 0x1D0],    #4-T
    [0x1B0, 0x1B0, 0x1B0, 0x1B0], #5-0
    [0x198, 0xB4, 0x198, 0xB4],   #6-Z
    [0xF0, 0x132, 0xF0, 0x132],   #7-S
])

#リスタート画面の表示
w = [150, 150, 150]
e = [0, 0, 0]

re = [
    e, e, e, e, e, e, e, e,
    w, e, w, e, e, w, w, e,
    w, w, e, w, w, e, e, w,
    w, e, e, e, w, w, w, w,
    w, e, e, e, w, e, e, e,
    w, e, e, e, w, e, e, w,
    w, e, e, e, e, w, w, e,
    e, e, e, e, e, e, e, e,
]

#テトロミノの変数の定義
activeTetro_x = None
activeTetro_y = None
activeTetro_shape = None
activeTetro_col = None
activeTetro_dir = None

#テトリミノの生成
def generateBlock():
    global activeTetro_x, activeTetro_y, activeTetro_shape, activeTetro_col, activeTetro_dir
    activeTetro_x = 1
    activeTetro_y = 5
    activeTetro_shape = np.random.randint(0, 7)
    activeTetro_col = np.random.randint(1, 8)
    activeTetro_dir = np.random.randint(0, 3)

#テトリミノの描画
def drawActiveTetro():
    k = 3
    for i in range(activeTetro_y -1, activeTetro_y + 2):
        m = 1
        for j in range(activeTetro_x - 1, activeTetro_y + 2):
            if(tetroType[activeTetro_shape][activeTetro_dir] & 1 << ((k*3)-m)):
                if(j-1 >= 0):
                    sense.set_pixel(i-1, j-1, tetroColor[activeTetro_col])
            m += 1
        k -= 1

#テトリミノの衝突判定
def checkMove(dx, dy):
    k = 3
    for i in range(activeTetro_y - 1, activeTetro_y + 2):
        m = 1
        for j in range(activeTetro_x - 1, activeTetro_y + 2):
            if(tetroType[activeTetro_shape][activeTetro_dir] & 1 << ((k*3)-m)):
                if(playfield[i + dy][j + dx] != 0):
                    return True
            m += 1
        k -= 1
    return False

#テトリミノの固定
def fixTetro():
    k = 3
    for i in range(activeTetro_y - 1, activeTetro_y + 2):
        m = 1
        for j in range(activeTetro_x - 1, activeTetro_x + 2):
            if(tetroType[activeTetro_shape][activeTetro_dir] & 1 << ((k*3)-m)):
                playfield[i][j] = activeTetro_shape + 1
            m += 1
        k -= 1

#フィールドの描画
def drawPlayfield():
    for i in range(0, 8):
        for j in range(0,8):
            sense.set_pixel(i, j, tetroColor[playfield[i+1][j+1]])

#ラインの消去
def checkLine():
    lineCount = 0
    i = 8
    while i > 0:
        brickCount = 0
        for j in range(1, 9):
            if playfield[j][i] != 0:
                brickCount += 1
        if brickCount == 8:
            for j in range(1, 9):
                playfield[j][i] = 0
            lineCount += 1
            for k in range(i, 1, -1):
                for m in range(1, 9):
                    playfield[m][k] = playfield[m][k-1]
            i += 1
        i -= 1
    return lineCount

#フィールドのクリア
def clearPlayfield():
    for i in range(1, 9):
        for j in range(1, 9):
            playfield[i][j] = 0

#ゲームリスタート
def restartGame():
    global score
    clearPlayfield()
    score = 0
    generateBlock()

#
generateBlock()


#main関数
while True:
    ct = time.time()
    dt = ct - lft
    lft = ct
    timeCounter += dt

    events = sense.stick.get_events()
    if events:
        for e in events:
            #左へ移動
            if e.direction == left_key and e.action == pressed:
                if not checkMove(0, -1):
                    activeTetro_y -= 1
            #右へ移動
            if e.direction == right_key and e.action == pressed:
                if not checkMove(0, 1):
                    activeTetro_y += 1
            #テトリミノの回転
            if e.direction == up_key and e.action == pressed:
                tmpDir = activeTetro_dir
                activeTetro_dir = (activeTetro_dir + 1) % 4
                if checkMove(0, 0):
                    activeTetro_dir = tmpDir
            #落下速度up
            if e.direction == down_key and e.action == pressed:
                interval = gameSpeed / 5
            #速度を戻す
            if e.direction == down_key and e.action == released:
                interval = gameSpeed
            
            #
            if e.direction == up_key and e.action == pressed and gameOver:
                restartGame()
                gameOver = False
            #
            if e.direction == down_key and e.action == pressed and gameOver:
                sense.clear()
                sys.exit()

    if(timeCounter > interval):
        timeCounter = 0
        if not gameOver:
            if not checkMove(1, 0):
                activeTetro_x += 1
            else:
                fixTetro()
                linesDestroyed = checkLine()
                if linesDestroyed == 1:
                    score += 1
                elif linesDestroyed == 2:
                    score += 10
                elif linesDestroyed == 3:
                    score += 30
                generateBlock()
                if checkMove(0, 0):
                    for k in range(0, 2):
                        sense.clear(255, 0, 0)
                        time.sleep(0.2)
                        sense.clear(255, 255, 255)
                        time.sleep(0.2)
                    sense.show_message("GAME OVER!",0.04)
                    msg = str(score) + "pts!"
                    sense.show_message(msg, 0.06)
                    clearPlayfield()
                    gameOver = True
            drawPlayfield()
            drawActiveTetro()
        else:
            sense.set_pixels(re)
            
            
            
            
------------------------------------------------------------------------------------------------------------------
import time
import sense_hat
import numpy as np
import sys
from random import randint

sense = sense_hat.SenseHat()
sense.clear()

#variables for convenience
left_key = sense_hat.DIRECTION_LEFT
right_key = sense_hat.DIRECTION_RIGHT
up_key = sense_hat.DIRECTION_UP
down_key = sense_hat.DIRECTION_DOWN
middle_key = sense_hat.DIRECTION_MIDDLE
pressed = sense_hat.ACTION_PRESSED
released = sense_hat.ACTION_RELEASED

#width and height of LED matrix, assumed square
playfieldSize = 10

#speed of game
gameSpeed = 0.5

#variables that need to be declared before main game loop
lft = 0.0
timeCounter = 0.0
score = 0
interval = gameSpeed
gameOver = False

playfield = np.zeros((playfieldSize,playfieldSize))

#creating borders outside of LED matrix
for i in range(0,playfieldSize):
    #playfield[i][0] = 1
    playfield[i][playfieldSize-1] = 1
    playfield[0][i] = 1
    playfield[playfieldSize-1][i] = 1

#block types in hexadecimal
#e.g.
#   010
#   010
#   010 is straight, vertical, 3 block line
#   what makes 010010010 written side by side
#   010010010(2) = 92(16) so 0x92 is it
blockData = np.array([
    [0x38, 0x92, 0x38, 0x92], #I
    [0x3A, 0xB2, 0xB8, 0x9A], #T
    [0xD8, 0xD8, 0xD8, 0xD8], #O
    [0x98, 0xD0, 0xC8, 0x58]  #L
    ])

#colors for corresponding block types
blockColors = {
    0 : (0,0,0),
    1 : (255,0,0),
    2 : (0,255,0),
    3 : (0,0,255),
    4 : (0,255,255)
}

w=[150,150,150]
e=[0,0,0]

arrow=[e,e,e,w,w,e,e,e,
e,e,w,w,w,w,e,e,
e,w,e,w,w,e,w,e,
w,e,e,w,w,e,e,w,
e,e,e,w,w,e,e,e,
e,e,e,w,w,e,e,e,
e,e,e,w,w,e,e,e,
e,e,e,w,w,e,e,e]


activeBlock_x = None
activeBlock_y = None
activeBlock_type = None
activeBlock_dir = None

def generateBlock():
    global activeBlock_x, activeBlock_y, activeBlock_type, activeBlock_dir
    activeBlock_x = 1
    activeBlock_y = 5
    activeBlock_type = randint(0,blockData.shape[0]-1)
    activeBlock_dir = randint(0,3)

def drawActiveBlock():
    k = 3
    for i in range(activeBlock_y - 1, activeBlock_y + 2):
        m = 1
        for j in range(activeBlock_x -1, activeBlock_x + 2):
            #print(i,j)
            if(blockData[activeBlock_type][activeBlock_dir] & 1 << ((k * 3) - m)):
                if(j - 1 >= 0):
                    sense.set_pixel(i-1, j-1, blockColors[activeBlock_type + 1])
            m = m + 1
        k = k - 1

def checkCollision(dx, dy):
    k = 3
    for i in range(activeBlock_y - 1, activeBlock_y + 2):
        m = 1
        for j in range(activeBlock_x -1, activeBlock_x + 2):
            #print(i,j)
            if(blockData[activeBlock_type][activeBlock_dir] & 1 << ((k * 3) - m)):
                if(playfield[i + dy][j + dx] != 0):
                    return True
            m = m + 1
        k = k - 1
    return False

def lockBlock():
    k = 3
    for i in range(activeBlock_y - 1, activeBlock_y + 2):
        m = 1
        for j in range(activeBlock_x -1, activeBlock_x + 2):
            if(blockData[activeBlock_type][activeBlock_dir] & 1 << ((k * 3) - m)):
                playfield[i][j] = activeBlock_type + 1
            m = m + 1
        k = k - 1

def drawPlayfield():
    for i in range(0,8):
        for j in range(0,8):
            sense.set_pixel(i, j, blockColors[playfield[i+1][j+1]])   

def checkForLine():
    lineCount = 0
    i = 8
    while i > 0:
        brickCount = 0
        for j in range(1, 9):
            if playfield[j][i] != 0:
                brickCount += 1
        if brickCount == 8:
            for j in range (1, 9):
                playfield[j][i] = 0
            lineCount += 1
            for k in range (i, 1, -1):
                for m in range (1, 9):
                    playfield[m][k] = playfield[m][k-1]
            i += 1
        i -= 1
    return lineCount

def clearPlayground():
    for i in range(1,9):
        for j in range(1,9):
            playfield[i][j] = 0

def restartGame():
    global score
    clearPlayground()
    score = 0
    generateBlock()

# generate first block, no need to check for collision at start
generateBlock()

#main game loop
while True:
    # dt is the time delta in seconds (float).
    ct = time.time()
    dt = ct - lft
    lft = ct
    timeCounter += dt
    
    events = sense.stick.get_events()
    if events:
        for e in events:
            #   Moving a block left
            if e.direction == left_key and e.action == pressed:
                if not checkCollision(0,-1):
                    activeBlock_y -= 1

            #   Moving a block right
            if e.direction == right_key and e.action == pressed:
                if not checkCollision(0,1):
                    activeBlock_y += 1

            #   Rotating a block
            if e.direction == up_key and e.action == pressed:
                tmpDir = activeBlock_dir
                activeBlock_dir = (activeBlock_dir + 1) % 4
                if checkCollision(0,0):
                    activeBlock_dir = tmpDir

            #   Speeding up a block
            if e.direction == down_key and e.action == pressed:
                interval = gameSpeed/5
            
            #   Resetting back to normal speed
            if e.direction == down_key and e.action == released:
                interval = gameSpeed

            if e.direction == up_key and e.action == pressed and gameOver:
                restartGame()
                gameOver = False

            if e.direction == down_key and e.action == pressed and gameOver:
                sense.clear()
                sys.exit()

    if(timeCounter > interval):
        timeCounter = 0
        if not gameOver:
            if not checkCollision(1,0):
                activeBlock_x += 1
            else:
                lockBlock()
                linesDestroyed = checkForLine()
                if linesDestroyed == 1:
                    score += 4
                elif linesDestroyed == 2:
                    score += 10
                elif linesDestroyed == 3:
                    score += 30
                generateBlock()
                if checkCollision(0,0):
                    for k in range (0, 2):
                        sense.clear(255,0,0)
                        time.sleep(0.2)
                        sense.clear(255,255,255)
                        time.sleep(0.2)
                    sense.show_message("GAME OVER", scroll_speed=0.04)
                    msg = str(score) + " pts!"
                    sense.show_message(msg, scroll_speed=0.07)
                    clearPlayground();
                    gameOver = True 
            drawPlayfield()
            drawActiveBlock()
        else:
            sense.set_pixels(arrow)

