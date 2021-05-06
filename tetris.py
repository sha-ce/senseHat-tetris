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

#スタートの座標
start_x = playfieldSize//2 - tetroSize//2
start_y = 0
#テトリミノの座標
tetro_x = start_x
tetro_y = start_y







#テトロミノの描画
def drawTetro():
    tetorCol = np.random.randint(1, 8)   #色
    tetroShape = np.random.randint(1, 8) #形
    tetro = tetroType[tetroShape]        #テトリミノ本体
    for j in range(0, 4):
        for k in range(0, 4):
            if tetroType[tetroShape][j][k] == 1:
                sense.set_pixel(k + start_x, j + start_y, tetroColor[tetorCol])
    return tetro

#ブロックの衝突判定
#def checkMove():

#テトリミノの回転
#def rotate():

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
                tetroMap(-1, 0)
            #右への移動
            if e.direction == right_key and e.action == pressed:
                tetroMap(1, 0)
            #テトロの回転
            #if e.direction == up_key and e.action == pressed:
            #テトロの速度up
            #if e.direction == down_key and e.action == pressed:
            #テトロの速度を戻す
            #if e.direction == down_key and e.action == released:
            
#テスト
drawTetro()
while True:
    joystick()



#main関数
#while True:
