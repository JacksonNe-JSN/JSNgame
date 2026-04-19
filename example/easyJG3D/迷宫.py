import LIBbase.JSNgame as jg
from LIBbase.JSNgame.third_D import Simple3DEngine
from tkinter import messagebox as mg
import time
import pygame as pg

screen = jg.Screen((800,600),icon="logo.bmp",title="迷宫")
event = jg.event
Event = jg.Event
st = time.time()

# 初始化引擎
game = Simple3DEngine(screen.screen,start_pos=(1.5, 1.5),
                      start_angle=0.5,see=10)
# 天空、地板渲染未完成
# 定义墙面颜色和世界布局
game.wall(
    color={
        1: "./d_wood.jpg",  # 红色墙面
        2: "./glass.png",
        3: "./glass.png",
        4: (0, 255, 0),# 绿色墙面
    },
    world_layout=[
        [1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1]
    ]
)

game.set_longway([155,155,155])
game.set_longway([155,155,155],'up')

# 启动游戏循环
a = 1
n = 0
game.load([])

# 帧率计算相关变量
last_time = time.time()
frame_count = 0
fps = 0

while a != "QUIT":
    time.sleep(0.01666)
    n += 1
    t = time.time() - st
    c = game.move()
    a = c[0]
    
    # 计算帧率
    current_time = time.time()
    frame_count += 1
    
    # 每0.5秒更新一次帧率显示
    if current_time - last_time >= 0.5:
        fps = frame_count / (current_time - last_time)
        frame_count = 0
        last_time = current_time
    
    # 显示帧率
    screen.word(f"FPS: {fps:.1f}", plc=[10, 10], big=30)
    
    screen.load()
    
    try:
        if c[1][0] <= 18.89928619 and c[1][1] >= 19.72566504 and c[1][0] >= 17.97691718 and c[1][1] <= 20:
            mg._show("JSNgame","you win!\n用时{}".format(t))
            break
    except:
        break

jg.exit()
