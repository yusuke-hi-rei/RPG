import pygame
import sys
import random

BLACK = (0, 0, 0)

MAZE_W = 11
MAZE_H = 9
maze = []

for y in range(MAZE_H):
    maze.append([0]*MAZE_W)

DUNGEON_W = MAZE_W*3
DUNGEON_H = MAZE_H*3
dungeon = []
for y in range(DUNGEON_H):
    dungeon.append([0]*DUNGEON_W)

imgWall   = pygame.image.load("wall.png")
imgFloor  = pygame.image.load("floor.png")
imgPlayer = pygame.image.load("player.png")

pl_x = 4
pl_y = 4


def make_dungeon():
    XP = [ 0, 1, 0, -1]
    YP = [-1, 0, 1,  0]

    # 周りの壁
    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[MAZE_H-1][x] = 1
    for y in range(1, MAZE_H-1):
        maze[y][0] = 1
        maze[y][MAZE_W-1] = 1

    # 中を何もない状態に
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            maze[y][x] = 0

    # 柱
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            maze[y][x] = 1

    # 柱から上下左右に壁を作る
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            d = random.randint(0, 3)
            if x > 2:
                # 二列目からは左に壁を作成しない
                d = random.randint(0, 2)
            maze[y+YP[d]][x+XP[d]] = 1

    # 迷路からダンジョンを作成
    # 全体を壁にする
    for y in range(DUNGEON_H):
        for x in range(DUNGEON_W):
            dungeon[y][x] = 9
    # 部屋と通路の配置
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            dx = x*3+1
            dy = y*3+1
            if maze[y][x] == 0:
                if random.randint(0, 99) < 20:
                    # 部屋を作成
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy+ry][dx+rx] = 0
                else:
                    # 通路を作成
                    dungeon[dy][dx] = 0
                    if maze[y-1][x] == 0:
                        dungeon[dy-1][dx] = 0
                    if maze[y+1][x] == 0:
                        dungeon[dy+1][dx] = 0
                    if maze[y][x-1] == 0:
                        dungeon[dy][dx-1] = 0
                    if maze[y][x+1] == 0:
                        dungeon[dy][dx+1] = 0


# ダンジョンを描く関数
# @param bg screen
def draw_dungeon(bg):
    # スクリーン全体をクリアする
    bg.fill(BLACK)
    for y in range(-5, 6):
        for x in range(-5, 6):
            X = (x+5)*16
            Y = (y+5)*16
            # ダンジョンのマス目のXY座標
            dx = pl_x + x
            dy = pl_y + y
            if 0 <= dx and dx < DUNGEON_W and 0 <= dy and dy < DUNGEON_H:
                if dungeon[dy][dx] == 0:
                    # 床
                    bg.blit(imgFloor, [X, Y])
                if dungeon[dy][dx] == 9:
                    # 壁
                    bg.blit(imgWall, [X, Y])
            if x == 0 and y == 0:
                # プレーヤーの描画
                bg.blit(imgPlayer, [X, Y-8])

# プレーヤーの移動関数
def move_player():
    global pl_x, pl_y
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] == 1:
        if dungeon[pl_y-1][pl_x] != 9:
            pl_y = pl_y-1
    if key[pygame.K_DOWN] == 1:
        if dungeon[pl_y+1][pl_x] != 9:
            pl_y = pl_y+1
    if key[pygame.K_LEFT] == 1:
        if dungeon[pl_y][pl_x-1] != 9:
            pl_x = pl_x-1
    if key[pygame.K_RIGHT] == 1:
        if dungeon[pl_y][pl_x+1] != 9:
            pl_x = pl_x+1


def main():
    # pygameモジュールの初期化
    pygame.init()
    # ウィンドウに表示されるタイトルを設定
    pygame.display.set_caption("ダンジョン")
    # スクリーンを初期化
    screen = pygame.display.set_mode((1056, 432))
    clock = pygame.time.Clock()

    # 迷路作成関数
    make_dungeon()

    while True:
        # pygameのイベントを繰り返しで処理する
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # ウィンドウの✖ボタンをクリック
                # pygameのモジュールの初期化を解除
                pygame.quit()
                # プログラムを終了
                sys.exit()

        move_player()
        draw_dungeon(screen)

        # 画面更新
        pygame.display.update()
        # フレームレートを設定する
        clock.tick(5)


if __name__ == "__main__":
    main()