#必要なライブラリをimport
import sense_hat
import numpy as np

sense = sense_hat.SenseHat()
sense.clear()
sense.set_rotation(90)

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

#変数
lines = 0
score = 0
interbal = gameSpeed
gameOver = False


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
    [],             #空っぽ
    [
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]   #1-I
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
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0],
        [0,0,0,0]   #5-O
    ],
    [
        [1,1,0,0],
        [0,1,1,0],
        [0,0,0,0],
        [0,0,0,0]   #6-Z
    ],
    [
        [0,1,1,0],
        [1,1,0,0],
        [0,0,0,0],
        [0,0,0,0]   #7-S
    ],
])




#テトリミノのサイズ
tetroSize = 4


tetroShape = np.random.randint(1, 8) #形
tetroCol   = np.random.randint(1, 8) #色
#テトリミノ本体
tetro = tetroType[tetroShape]

#スタート地点
start_x = playfieldSize//2 - tetroSize//2
start_y = 0

#テトリミノの座標
tetro_x = start_x
tetro_y = start_y



#テトロミノを描画
def drawTetro():
    for y in range(0, tetroSize):
        for x in range(0, tetroSize):
            if tetro[y][x]:
                sense.set_pixel(x + start_x, y + start_y, tetroColor[tetroCol])
    if gameOver:
        sense.show_message("Game Over", 0.05, [255, 0, 0], [0, 0, 0])

#ブロックの衝突判定
def checkMove(mx, my, ntetro):
    if ntetro == None:
        ntetro = tetro
    for y in range(0, tetroSize):
        for x in range(0, tetroSize):
            nx = tetro_x + mx + x
            ny = tetro_y + my + y
            if ntetro[y][x]:
                if ny < 0 or nx < 0 or ny >= playfieldSize or nx >= playfieldSize or playfield[ny][nx]:
                    return False
    return True

#テトリミノの回転
def rotate():
    ntetro = []
    for y in range(0, tetroSize):
        ntetro[y] = []
        for x in range(0, tetroSize):
            ntetro[y][x] = tetro[tetroSize-1 - x][y]
    return ntetro

#ブロックの固定
def fixTetro():
    for y in range(0, tetroSize):
        for x in range(0, tetroSize):
            if tetro[y][x]:
                playfield[tetro_y + y][tetro_x + x] = tetroShape

#ラインの消去
def checkLine():
    linec = 0
    for y in range(0, playfieldSize):
        frag = True
        for x in range(0, playfieldSize):
            if not playfield[y][x]:
                frag == False
                break
        if frag:
            linec += 1
            for ny in range(0, y):
                for nx in range(0, playfieldSize):
                    playfield[ny][nx] = playfield[ny-1][nx]

#テトリミノの落下
def dropTetro():
    if gameOver:
        return

    if checkMove(0, 1):
        tetro_y += 1
    else:
        fixTetro()
        checkLine()

        tetroShape = np.random.randint(1, 8)
        tetro = tetroType[tetroShape]

        tetro_x = start_x
        tetro_y = start_y

        if not checkMove(0, 0):
            gameOver = True

    drawTetro()






#ジョイスティックでの操作
def moveRotation():
    if gameOver:
        return

    events = sense.stick.get_events()
    if events:
        for e in events:
            #左
            if e.direction == left_key and e.action == pressed:
                if checkMove(-1, 0):
                    tetro_x -= 1
                    break
            #右
            if e.direction == right_key and e.action == pressed:
                if checkMove(1, 0):
                    tetro_x += 1
                    break
            #上
            if e.direction == up_key and e.action == pressed:
                ntetro = rotate()
                if checkMove(0, 0, ntetro):
                    tetro = ntetro
                    break
            #下
            if e.direction == down_key and e.action == pressed:
                if checkMove(0, 1):
                    tetro_y += 1
                    break

#main関数
drawTetro()
while True:
    dropTetro()
    moveRotation()
