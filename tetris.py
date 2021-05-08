#必要なライブラリをimport
import sense_hat
import numpy as np

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
        [0,0,0,0],
        [1,1,1,1],
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
        [0,0,0,0],
        [0,1,1,0],
        [0,1,1,0],
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
blockSize = 4

#テトリミノの色と形
tetroCol = np.random.randint(1, 8)   #色
tetroShape = np.random.randint(1, 8) #形

#スタートの座標
start_x = playfieldSize//2 - tetroSize//2
start_y = 0



#テトロミノの描画
def drawTetro():
    global tetroCol
    global tetroShape
    tetroCol = np.random.randint(1, 8)   #色
    tetroShape = np.random.randint(1, 8) #形
    for j in range(0, tetroSize):
        for k in range(0, tetroSize):
            if tetroType[tetroShape][j][k] == 1:
                sense.set_pixel(k + start_x, j + start_y, tetroColor[tetroCol])

#テトリミノの移動
def moveBlock(dx, dy):
    pixelList = sense.get_pixels()
    array = []
    for i in range(0, 64):
        if pixelList[i] != [0, 0, 0]:
            array.append(i)
    sense.clear()
    for j in range(0, blockSize):
        #壁にテトリミノが衝突した場合移動はさせない
        if(array[j]%8 + dx < 0 or array[j]%8 + dx >= playfieldSize or array[j]//8 + dy < 0 or array[j]//8 + dy >= playfieldSize):
            sense.set_pixels(pixelList)
            break
        else:
            sense.set_pixel(array[j]%8 + dx, array[j]//8 + dy, pixelList[array[j]])

#テトリミノの回転
def rotate():
    pixelList = sense.get_pixels()
    array = []
    tetro_rot = np.rot90(tetroType[tetroShape])
    for i in range(0, 64):
        if pixelList[i] != [0, 0, 0]:
            array.append(i)
    sense.clear()
    for j in range(0, blockSize):
        for k in range(0, tetroSize):
            for l in range(0, tetroSize):
                if tetro_rot[k][l] == 1:
                    sense.set_pixel(array[j]%8 + l, array[j]//8 + k, pixelList[array[j]])



#ブロックの固定
#def fixBlock():

#ラインの消去
#def checkLine():

#テトリミノの落下
#def dropTetro():

#ジョイスティックでの操作
def joystick():
    events = sense.stick.get_events()
    if events:
        for e in events:
            #左への移動
            if e.direction == left_key and e.action == pressed:
                moveBlock(-1, 0)
            #右への移動
            if e.direction == right_key and e.action == pressed:
                moveBlock(1, 0)
            #テトロの回転
            if e.direction == up_key and e.action == pressed:
                rotate()
            #下への移動
            if e.direction == down_key and e.action == pressed:
                moveBlock(0, 1)
            
#テスト
drawTetro()
while True:
    joystick()



#main関数
#while True:
