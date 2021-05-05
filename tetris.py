import sense_hat
import numpy as np
import time
import random
from datetime import datetime
import sys

sense = SenseHat()
sense.clear()

#ジョイスティック設定
left_key   = sense_hat.DIRECTION_LEFT
right_key  = sense_hat.DIRECTION_RIGHT
up_key     = sense_hat.DIRECTION_UP
down_key   = sense_hat.DIRECTION_DOWN
middle_key = sense_hat.DIRECTION_MIDDLE
pressed    = sense_hat.ACTION_PRESSED
released   = sense_hat.ACTION_RELEASED

#フィールドサイズ
playfieldSize = 8
playfield = np.zeros((playfieldSize, playfieldSize))

#ゲームスピード
gameSpeed = 0.5

#main関数での変数
lft = 0.0
timeCounter = 0.0
score = 0
interbal = gameSpeed
gameOver = False

#境界線の設定
for i in range(0, playfieldSize):
    playfield[i][0] = 1
    playfield[i][playfieldSize-1] = 1
    playfield[0][i] = 1
    playfield[playfieldSize-1][i] = 1

#テトリスの色を定義
tetroColor = [
    [],
    [0, 255, 255],   #1-水
    [0, 0, 255],     #2-青
    [255, 0, 255],   #3-紫
    [255, 255, 0],   #4-黄
    [255, 0, 0],     #5-赤
    [0, 255, 0],     #6-緑
    [255, 255, 255], #7-白
]

#テトリミノの形を定義
tetroType = np.array([
    [],#空っぽ
    [
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0]  #1-I
    ],
    [
        [0,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,0,0]   #2-L
    ],
    [
        [0,0,1,0],
        [0,0,1,0],
        [0,1,1,0],
        [0,0,0,0]   #3-J
    ],
    [
        [0,1,0,0],
        [0,1,1,0],
        [0,1,0,0],
        [0,0,0,0]   #4-T
    ],
    [
        [0,0,0,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0]   #5-O
    ],
    [
        [0,0,0,0],
        [1,1,0,0],
        [0,1,1,0],
        [0,0,0,0]   #6-Z
    ],
    [
        [0,0,0,0],
        [0,1,1,0],
        [1,1,0,0],
        [0,0,0,0]   #7-S
    ],
])

#矢
w = [150, 150, 150]
e = [0, 0, 0]

arrow = [
    e, e, e, w, w, e, e, e,
    e, e, w, w, w, w, e, e,
    e, w, e, w, w, e, w, e,
    w, e, e, w, w, e, e, w, 
    e, e, e, w, w, e, e, e,
    e, e, e, w, w, e, e, e,
    e, e, e, w, w, e, e, e,
    e, e, e, w, w, e, e, e,
]


#描画しているテトリミノの設定
activeBlock_x    = None
activeBlock_y    = None
activeBlock_type = None
activeBlock_dir  = None

def generateTetro():
    global activeBlock_x, activeBlock_y, activeBlock_type, activeBlock_dir
    activeBlock_x = 1
    activeBlock_y = 5
    activeBlock_type = random.randint(0, tetroType[0]-1)
    activeBlock_dir  = random.randint(0, 3)

def drawActiveTetro():
    k = 3
    for i in range(activeBlock_y - 1, activeBlock_y + 2):
        m = 1
        for j in range(activeBlock_x - 1, activeBlock_x + 2):
            if(tetroType[activeBlock_type][activeBlock_dir] & 1 << ((k*3) - m)):
                if(j - 1 >= 0):
                    sense.set_pixel(i-1, j-1, tetroColor[activeBlock_type + 1])
            m += 1
        k -= 1

def checkCollision(dx, dy):
    k = 3
    for i in range(activeBlock_y - 1, activeBlock_y + 2):
        m = 1
        for j in range(activeBlock_x - 1, activeBlock_x + 2):
            if (tetroType[activeBlock_type][activeBlock_dir] & 1 << ((k*3) - m)):
                if(playfield[i+dy][j+dx] != 0):
                    return True
            m += 1
        k -= 1
    return False

def lockTetro():
    k = 3
    for i in range(activeBlock_y - 1, activeBlock_y + 2):
        m = 1
        for j in range(activeBlock_x - 1, activeBlock_x + 2):
            if(tetroType[activeBlock_type][activeBlock_dir] & 1 << ((k*3) - m)):
                playfield[i][j] = activeBlock_type + 1
            m += 1
        k -= 1

def drawPlayfield():
    for i in range(0, 8):
        for j in range(0, 8):
            sense.set_pixel(i, j, tetroColor[playfield[i+1][j+1]])

def checkForLine():
    linecount = 0
    i = 8
    while i > 0:
        brickCount = 0
        for j in range(1, 9):
            if playfield[j][i] != 0:
                brickCount += 1
        if brickCount == 8:
            for j in range(1, 9):
                playfield[j][i] = 0
            linecount += 1
            for k in range(i, 1, -1):
                for m in range(1, 9):
                    playfield[m][k] = playfield[m][k-1]
            i += 1
        i -= 1
    return linecount

def clearPlayground():
    for i in range(1, 9):
        for j in range(1, 9):
            playfield[i][j] = 0

def restartGame():
    global score
    clearPlayground()
    score = 0
    generateTetro()

generateTetro()

#main関数
while True:
    ct = time.time()
    dt = ct - lft
    ltf = ct
    timeCounter += dt

    events = sense.stick.get_events()
    if events:
        for e in events:
            #左への移動
            if e.direction == left_key and e.action == pressed:
                if not checkCollision(0, -1):
                    activeBlock_y -= 1
            #右への移動
            if e.direction == right_key and e.action == pressed:
                if not checkCollision(0, 1):
                    activeBlock_y += 1
            #テトロミノの回転
            if e.direction == up_key and e.action == pressed:
                tmpDir = activeBlock_dir
                activeBlock_dir = (activeBlock_dir + 1) % 4
                if checkCollision(0, 0):
                    activeBlock_dir = tmpDir
            #テトロミノを落とす
            if e.direction == down_key and e.action == pressed:
                interval = gameSpeed / 5
            #スピードを戻す
            if e.direction == down_key and e.action == released:
                interval = gameSpeed
            
            if e.direction == up_key and e.action == pressed and gameOver:
                restartGame()
                gameOver = False
            
            if e.direction == down_key and e.action == pressed and gameOver:
                sense.clear()
                sys.exit()

    if(timeCounter > interbal):
        timeCounter = 0
        if not gameOver:
            if not checkCollision(1, 0):
                activeBlock_x += 1
            else:
                lockTetro()
                linesDestroyed = checkForLine()
                if linesDestroyed == 1:
                    score += 1
                elif linesDestroyed == 2:
                    score += 2
                elif linesDestroyed == 3:
                    score += 4
                generateTetro()
                if checkCollision(0,0):
                    for k in range(0, 2):
                        sense.clear(255, 0, 0)
                        time.sleep(0.2)
                        sense.clear(255, 255, 255)
                        time.sleep(0.2)
                    sense.show_message("GAME OVER", scroll_speed = 0.04)
                    msg = str(score) + "points!"
                    sense.show_message(msg, scroll_speed = 0.07)
                    clearPlayground()
                    gameOver = True
            drawPlayfield()
            drawActiveTetro()
        else:
            sense.set_pixels(arrow)

                
