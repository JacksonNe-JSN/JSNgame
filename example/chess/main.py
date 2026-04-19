from LIBbase import JSNgame as jg
from LIBbase.JSNgame.message import Message as mx
from LIBbase.JSNgame import AI_tree as ait
import tkinter as tk
import os, random, time
import numpy as np
from LIBbase.JSNgame.AI_tree import Jai

# =====init=====#
def init():
    global screen, event, Event, mixer, side, world
    screen = jg.Screen((700, 700), icon='./icon.ico', title='国际象棋v0.0.3')
    event = jg.event
    Event = jg.Event
    mixer = jg.mixer()
    side = '白'

    world = [
        ['黑车', '黑马', '黑象', '黑后', '黑王', '黑象', '黑马', '黑车'],
        ['黑兵'] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        ['白兵'] * 8,
        ['白车', '白马', '白象', '白后', '白王', '白象', '白马', '白车']
    ]

    print(world)


# +++++++++++++++++++++++++++++++++AI++++++++++++++++++++++++++++++++#
# 棋子价值字典（仅用于奖励计算）
piece_values = {
    '兵': 1,
    '马': 3,
    '象': 3,
    '车': 5,
    '后': 9,
    '王': 1000
}

# 棋子到整数编码的映射（与训练程序保持一致）
piece_to_code = {
    None: 0,
    '白兵': 1, '白马': 2, '白象': 3, '白车': 4, '白后': 5, '白王': 6,
    '黑兵': 7, '黑马': 8, '黑象': 9, '黑车': 10, '黑后': 11, '黑王': 12
}

def board_to_state(world):
    """
    将棋盘转换为纯数值的状态字典，供 Jai 决策。
    特征集与训练程序完全一致，确保模型可加载。
    """
    state = {}
    
    # 1. 每个格子的棋子编码 (64个特征)
    for y in range(8):
        for x in range(8):
            piece = world[y][x]
            state[f"cell_{y}_{x}"] = piece_to_code.get(piece, 0)
    
    # 2. 双方子力数量
    white_pieces = 0
    black_pieces = 0
    for y in range(8):
        for x in range(8):
            piece = world[y][x]
            if piece:
                if piece.startswith('白'):
                    white_pieces += 1
                else:
                    black_pieces += 1
    state["white_pieces"] = white_pieces
    state["black_pieces"] = black_pieces
    
    # 注意：此处特征必须与训练程序中的 board_to_state 完全一致，
    # 不能包含 value_diff、center_* 等额外特征，否则会导致特征不一致错误。
    return state

def get_piece_value(piece_name):
    """获取棋子基础价值"""
    if piece_name and len(piece_name) > 1:
        return piece_values.get(piece_name[1:], 0)
    return 0

def find_king(world, side):
    """找到指定方的王位置"""
    for y in range(8):
        for x in range(8):
            piece = world[y][x]
            if piece and piece == f'{side}王':
                return (x, y)
    return None

def is_check(world, side):
    """检查某方是否被将军"""
    king_pos = find_king(world, side)
    if not king_pos:
        return False

    enemy_side = '白' if side == '黑' else '黑'
    for y in range(8):
        for x in range(8):
            piece = world[y][x]
            if piece and piece.startswith(enemy_side):
                moves = can_move(piece, [x, y])
                if [king_pos[0], king_pos[1]] in moves:
                    return True
    return False

def is_checkmate_after_move(action, world, side):
    """模拟走子后，敌方是否被将死（简化判断：被将军且无合法走子）"""
    x1, y1, x2, y2 = action
    enemy_side = '白' if side == '黑' else '黑'

    # 保存棋盘状态
    original_piece = world[y2][x2]
    moving_piece = world[y1][x1]

    # 执行移动
    world[y2][x2] = moving_piece
    world[y1][x1] = None

    # 检查敌方是否被将军
    check = is_check(world, enemy_side)
    checkmate = False
    if check:
        # 检查敌方是否有任何合法走子
        has_legal = False
        for y in range(8):
            for x in range(8):
                piece = world[y][x]
                if piece and piece.startswith(enemy_side):
                    moves = can_move(piece, [x, y])
                    for move in moves:
                        tx, ty = move
                        target_save = world[ty][tx]
                        world[ty][tx] = piece
                        world[y][x] = None
                        if not is_check(world, enemy_side):
                            has_legal = True
                        world[y][x] = piece
                        world[ty][tx] = target_save
                        if has_legal:
                            break
                if has_legal:
                    break
        if not has_legal:
            checkmate = True

    # 恢复棋盘
    world[y1][x1] = moving_piece
    world[y2][x2] = original_piece
    return checkmate

def calculate_reward(action, world, side):
    """
    计算一个动作的奖励分数（范围建议 -10 到 10）
    """
    x1, y1, x2, y2 = action
    enemy_side = '白' if side == '黑' else '黑'
    moving_piece = world[y1][x1]
    target_piece = world[y2][x2]

    reward = 0.0

    # 1. 吃子奖励
    if target_piece and target_piece.startswith(enemy_side):
        reward += get_piece_value(target_piece) * 0.8

    # 2. 将军奖励
    original_target = world[y2][x2]
    world[y2][x2] = moving_piece
    world[y1][x1] = None
    if is_check(world, enemy_side):
        reward += 3.0
    if is_checkmate_after_move(action, world, side):
        reward += 10.0
    world[y1][x1] = moving_piece
    world[y2][x2] = original_target

    # 3. 中心控制奖励
    if (2 <= x2 <= 5) and (2 <= y2 <= 5):
        reward += 0.2
    if (3 <= x2 <= 4) and (3 <= y2 <= 4):
        reward += 0.3

    # 4. 解围奖励
    if is_check(world, side):
        original_target = world[y2][x2]
        world[y2][x2] = moving_piece
        world[y1][x1] = None
        if not is_check(world, side):
            reward += 4.0
        world[y1][x1] = moving_piece
        world[y2][x2] = original_target

    # 5. 兵升变奖励
    if moving_piece and moving_piece[1:] == '兵':
        if (side == '白' and y2 == 0) or (side == '黑' and y2 == 7):
            reward += 8.0

    return reward

# 黑方AI实例
_jai_black = None

def _init_jai():
    global _jai_black
    if _jai_black is None:
        # 训练模式设为 'use' 以避免对局中继续训练（推荐）
        _jai_black = Jai("chess_black.jai", "train")
        _jai_black.set_print(0)  # 静默模式

def JSN_AI(world, side='黑'):
    """
    国际象棋AI函数（固定执黑）
    """
    _init_jai()
    ai = _jai_black

    # 1. 收集所有合法动作
    all_actions = []
    for y in range(8):
        for x in range(8):
            piece = world[y][x]
            if piece and piece.startswith('黑'):   # 固定黑方
                moves = can_move(piece, [x, y])
                for move in moves:
                    if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                        all_actions.append((x, y, move[0], move[1]))

    if not all_actions:
        return [[0, 0], [0, 0], None]

    # 2. 构建当前状态字典（纯数值）
    state = board_to_state(world)

    # 3. 记录上次决策信息（用于反馈学习，但 use 模式下学习效果有限）
    if not hasattr(JSN_AI, "last_state"):
        JSN_AI.last_state = None
        JSN_AI.last_action = None
        JSN_AI.last_action_index = None

    # 如果有上一轮的状态和动作，给予反馈
    if JSN_AI.last_state is not None and JSN_AI.last_action is not None:
        reward = calculate_reward(JSN_AI.last_action, world, '黑')
        ai.report(JSN_AI.last_state, JSN_AI.last_action_index, reward)

    # 4. AI 选择动作
    action_index = ai.out(state, len(all_actions))

    # 5. 保存本次决策信息
    JSN_AI.last_state = state
    JSN_AI.last_action = all_actions[action_index]
    JSN_AI.last_action_index = action_index

    # 6. 解析动作并返回
    x1, y1, x2, y2 = all_actions[action_index]
    piece = world[y1][x1]
    return [[y1, x1], [y2, x2], piece]

def use_jAI(side='黑'):
    global world
    print('jAI:让我看看')
    mOve = JSN_AI(world, side='黑')
    print('jAI:有了!', mOve)
    move(mOve[0], mOve[1])
    print('jAI:我动!')

# +++++++++++++++++++++++++++++++++AI++++++++++++++++++++++++++++++++#


pos = (0, 0)
photo = {'qp': './image/bgp.png',
         'zx': './image/准星.png',
         }
Sound = {'get': './sound/get.wav',
         'choose': './sound/choose.wav',
         'eat': './sound/eat.wav'}


def button(pos, plc, size):
    if pos[0] >= plc[0] and pos[0] <= plc[0] + size[0] and pos[1] > plc[1] and pos[1] < plc[1] + size[1]:
        return True
    else:
        return False


Get = [None, -1, -1]
GET = [None, -1, -1]
Move = []


def get():
    global world, pos
    n = [0, 0]
    for i in range(8):
        for j in range(8):
            if button(pos, (52.5 + j * 75, 52.5 + i * 75), (75, 75)):
                return [world[i][j], j, i]
    return [None, -1, -1]


def show(moving=True):
    global pos, Move, teshu
    screen.fill((150, 150, 150))
    screen.blit(photo['qp'], [50, 50])

    n = [0, 0]
    for i in world:
        for j in i:
            if j != None and n != [GET[1], GET[2]]:
                screen.blit(f'./image/{j}.png', [n[0] * 75 + 52, n[1] * 75 + 52])
            n[0] += 1
        n[1] += 1
        n[0] = 0

    if Get[0] != None and world[Get[2]][Get[1]] != None and moving and Get[0][0:1] == side:
        screen.blit(f'./image/{world[Get[2]][Get[1]]}.png', (52.5 + Get[1] * 75, 49 + Get[2] * 75))

    for i in Move:
        if world[i[1]][i[0]] == None and [i[0], i[1]] not in teshu['过路兵']:
            if [get()[1], get()[2]] == i:
                screen.blit('./image/Rcan_move2.png', (i[0] * 75 + 72.5, i[1] * 75 + 72.5))
            else:
                screen.blit('./image/Rcan_move1.png', (i[0] * 75 + 72.5, i[1] * 75 + 72.5))
        else:
            if [get()[1], get()[2]] == i:
                screen.blit('./image/Gcan_move2.png', (i[0] * 75 + 72.5, i[1] * 75 + 72.5))
            else:
                screen.blit('./image/Gcan_move1.png', (i[0] * 75 + 72.5, i[1] * 75 + 72.5))
    screen.blit(photo['zx'], (pos[0] - 15, pos[1] - 15))
    for i in range(8):
        screen.word(str(i), plc=(0, 75 + i * 75), big=75, rgb=(255, 255, 255))
    for j in range(8):
        screen.word(str(j), plc=(75 + j * 75, 0), big=75, rgb=(255, 255, 255))

    screen.load()


G = [None, -1, -1]


def eVent():
    global Event, pos, Get, GET, Move, G, side
    for e in event.get():
        if event.test(e, Event['QUIT']) or event.test_key(e, Event['K_ESCAPE']): jg.exit()
        if event.test(e, Event['MOUSEBUTTONUP']) or event.test(e, Event['MOUSEBUTTONDOWN']) or event.test(e,
                                                                                                            Event['MOUSEMOTION']):
            pos = e.pos
            if GET[0] == None:
                Get = get()
                if Get != G and Get[0] != None:
                    mixer.sound(Sound['get'])
                G = Get
                Move = can_move(Get[0], (Get[1], Get[2]))
            elif Get:
                Get = GET
        else:
            pos = (999, 999)
        if event.test(e, Event['MOUSEBUTTONDOWN']):
            if Get[0] != None:
                if GET[0] == None and Get[0][0:1] == side:
                    GET = Get
                    mixer.sound(Sound['choose'])
                    Move = can_move(Get[0], (Get[1], Get[2]))
                    return
                elif [get()[1], get()[2]] in Move:
                    move((GET[2], GET[1]), [get()[2], get()[1]])
                else:
                    GET = [None, -1, -1]
                    Move = []
            else:
                GET = [None, -1, -1]
                Move = []


def J1(n):
    return 0 <= n < 8


def can_move(n, plc):
    global world, teshu
    if n == None or plc == None:
        return []
    teshu = {'过路兵': []}
    color = n[0]
    piece_type = n[1]
    x, y = plc[0], plc[1]
    possible_moves = []

    if piece_type == '王':
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = world[ny][nx]
                if target is None or target[0] != color:
                    possible_moves.append([nx, ny])

    elif piece_type == '后':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            step = 1
            while True:
                nx, ny = x + dx * step, y + dy * step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                target = world[ny][nx]
                if target is not None:
                    if target[0] != color:
                        possible_moves.append([nx, ny])
                    break
                else:
                    possible_moves.append([nx, ny])
                step += 1

    elif piece_type == '车':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            step = 1
            while True:
                nx, ny = x + dx * step, y + dy * step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                target = world[ny][nx]
                if target is not None:
                    if target[0] != color:
                        possible_moves.append([nx, ny])
                    break
                else:
                    possible_moves.append([nx, ny])
                step += 1

    elif piece_type == '象':
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            step = 1
            while True:
                nx, ny = x + dx * step, y + dy * step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                target = world[ny][nx]
                if target is not None:
                    if target[0] != color:
                        possible_moves.append([nx, ny])
                    break
                else:
                    possible_moves.append([nx, ny])
                step += 1

    elif piece_type == '马':
        candidates = [
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2),
            (x - 1, y + 2), (x - 1, y - 2)
        ]
        for (nx, ny) in candidates:
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = world[ny][nx]
                if target is None or target[0] != color:
                    possible_moves.append([nx, ny])

    elif piece_type == '兵':
        b = 1
        if color == '白':
            if J1(plc[1] - 1) and J1(plc[0]):
                if world[plc[1] - 1][plc[0]] == None:
                    possible_moves.append([plc[0], plc[1] - 1])
            if plc[1] == 6 and world[plc[1] - 2][plc[0]] == None and world[plc[1] - 1][plc[0]] == None:
                possible_moves.append([plc[0], plc[1] - 2])
            if J1(plc[1] - 1) and J1(plc[0] + 1):
                if str(world[plc[1] - 1][plc[0] + 1])[0:1] == '黑':
                    possible_moves.append([plc[0] + 1, plc[1] - 1])
                    b = 0
            if J1(plc[1] + 1) and J1(plc[0] - 1):
                if str(world[plc[1] - 1][plc[0] - 1])[0:1] == '黑':
                    possible_moves.append([plc[0] - 1, plc[1] - 1])
                    b = 0
            if b:
                try:
                    if world[plc[1]][plc[0] - 1] == '黑兵' and world[plc[0] - 1][plc[1] - 1] == None:
                        possible_moves.append([plc[0] - 1, plc[1] - 1])
                        teshu['过路兵'].append([plc[0] - 1, plc[1] - 1])
                except Exception as e:
                    pass
                try:
                    if world[plc[1]][plc[0] + 1] == '黑兵' and world[plc[0] + 1][plc[1] - 1] == None:
                        possible_moves.append([plc[0] + 1, plc[1] - 1])
                        teshu['过路兵'].append([plc[0] + 1, plc[1] - 1])
                except Exception as e:
                    pass
        elif color == '黑':
            if J1(plc[1] + 1) and J1(plc[0]):
                if world[plc[1] + 1][plc[0]] == None:
                    possible_moves.append([plc[0], plc[1] + 1])
            if plc[1] == 1 and world[plc[1] + 2][plc[0]] == None and world[plc[1] + 1][plc[0]] == None:
                possible_moves.append([plc[0], plc[1] + 2])
            if J1(plc[1] + 1) and J1(plc[0] + 1):
                if str(world[plc[1] + 1][plc[0] + 1])[0:1] == '白':
                    possible_moves.append([plc[0] + 1, plc[1] + 1])
                    b = 1
            if J1(plc[1] + 1) and J1(plc[0] - 1):
                if str(world[plc[1] + 1][plc[0] - 1])[0:1] == '白':
                    possible_moves.append([plc[0] - 1, plc[1] + 1])
                    b = 1
            if b:
                try:
                    if world[plc[1]][plc[0] - 1] == '白兵' and world[plc[0] - 1][plc[1] + 1] == None:
                        possible_moves.append([plc[0] - 1, plc[1] + 1])
                        teshu['过路兵'].append([plc[0] - 1, plc[1] + 1])
                except Exception as e:
                    pass
                try:
                    if world[plc[1]][plc[0] + 1] == '白兵' and world[plc[0] + 1][plc[1] + 1] == None:
                        possible_moves.append([plc[0] + 1, plc[1] + 1])
                        teshu['过路兵'].append([plc[0] + 1, plc[1] + 1])
                except Exception as e:
                    pass
    else:
        return []

    return possible_moves


def MOVe(n, plc, new_plc):
    w = [abs(new_plc[0] - plc[0]) / 5, abs(new_plc[1] - plc[1]) / 5]
    Plc = plc
    m = 5
    while m > 0:
        show(False)
        screen.blit('./image/{}.png'.format(n), (Plc[1] * 75 + 55.5, Plc[0] * 75 + 55.5))
        if Plc[0] < new_plc[0]:
            Plc[0] += w[0]
        if Plc[0] > new_plc[0]:
            Plc[0] -= w[0]
        if Plc[1] < new_plc[1]:
            Plc[1] += w[1]
        if Plc[1] > new_plc[1]:
            Plc[1] -= w[1]
        Plc[0] -= 0.5 * 1.5
        m -= 1
        screen.load()


def EAt(plc=None):
    global aI
    if plc != None and not aI:
        screen.TeXiao('ZhenDong', 20)
        screen.blit('./image/white_qi.png', [plc[1] * 75 + 52, plc[0] * 75 + 52])
        screen.load()
        mixer.sound('./sound/die.wav')


def move(plc, new_plc):
    global world, GET, Get, Move, teshu, side, a, aI, jAI
    W = world[plc[0]][plc[1]]
    color = W[0:1]
    if not aI or 1:
        MOVe(world[plc[0]][plc[1]], [plc[0], plc[1]], new_plc)
        mixer.sound(Sound['eat'])
    world[plc[0]][plc[1]] = None
    if world[new_plc[0]][new_plc[1]] != None:
        EAt([new_plc[0], new_plc[1]])
    world[new_plc[0]][new_plc[1]] = W

    for i in teshu['过路兵']:
        if [new_plc[1], new_plc[0]] == i:
            if color == '白':
                world[new_plc[0] + 1][new_plc[1]] = None
            elif color == '黑':
                world[new_plc[0] - 1][new_plc[1]] = None
            EAt()

    GET = [None, -1, -1]
    Get = [None, -1, -1]
    Move = []
    test()
    if side == '白':
        side = '黑'
        if jAI and ab == False:
            use_jAI()
    else:
        side = '白'


def test():
    global world, teshu, Move, ab, jAI
    eVent()
    wang = {'白王': [-999, -999], '黑王': [-999, -999]}
    for i in range(8):
        for j in range(8):
            if world[i][j] != None:
                if world[i][j][1:2] == '王':
                    wang[world[i][j]] = [i, j]
    check = []
    for i in range(8):
        for j in range(8):
            if world[i][j] != None:
                a = can_move(world[i][j], [j, i])
                for k in a:
                    if k == [wang['白王'][1], wang['白王'][0]] or k == [wang['黑王'][1], wang['黑王'][0]]:
                        if k == [wang['白王'][1], wang['白王'][0]]:
                            check.append([wang['白王'][1], wang['白王'][0]])
                        if k == [wang['黑王'][1], wang['黑王'][0]]:
                            check.append([wang['黑王'][1], wang['黑王'][0]])
                        check.append([j, i])

    if not aI:
        if check != []:
            mixer.sound('./sound/check.wav')
            for p in range(10):
                time.sleep(0.01)
                main()
                if p % 2 == 0:
                    for i in check:
                        screen.word('将军', plc=[240, 300], big=100, rgb=(0, 0, 0))
                        screen.word('将军', plc=[250, 300], big=100)
                        screen.blit('./image/white_qi.png', [i[0] * 75 + 52, i[1] * 75 + 52.5])
                    screen.load()
    for i in wang:
        if wang[i] == [-999, -999]:
            if i == '黑王':
                ab = '白'
            if i == '白王':
                ab = '黑'
    return wang


aI = False
jAI = True   # 启用黑方AI
dAI = False


def start():
    global ab, root, aI
    try:
        root.destroy()
    except:
        pass
    if not aI:
        mx.text('注意', '本游戏由JSN一人制作')
    init()
    ab = False
    Time = jg.Time()
    while ab == False:
        Time.FPS(100)
        main()

    if not aI:
        p = []
        if ab == '黑':
            ba = '白'
        else:
            ba = '黑'
        for i in range(8):
            for j in range(8):
                if str(world[i][j])[0:1] == ba:
                    p.append([i, j])
        random.shuffle(p)
        for i in p:
            time.sleep(0.03)
            main()
            mixer.sound('./sound/die.wav')
            screen.blit('./image/white_qi.png', [i[1] * 75 + 52, i[0] * 75 + 52.5])
            world[i[0]][i[1]] = None
            screen.TeXiao('ZhenDong', 10)
            screen.load()
        for i in test():
            if not aI:
                _jai_black.init()#触发学习
                jg.message.Message._show('游戏结束', '{}方胜利'.format(ab))
                return
            return


def start_JSNAI():
    global jAI
    jAI = True
    start()


def main():
    global ab
    show()
    eVent()


class menu():
    def __init__(self):
        global screen, world, root
        root = tk.Tk()
        root.title('选择模式')
        b1 = tk.Button(root, text="普通模式", font=('./image/zt.ttf', 50), command=start)
        b2 = tk.Button(root, text="JSN_AI", font=('./image/zt.ttf', 50), command=start_JSNAI)
        b1.pack()
        b2.pack()
        root.mainloop()


menu()

jg.Exit()
