import pygame
import random
import copy

"""
主要思路:
（1）蛇每走一步，就使用BFS计算游戏界面中每个位置（蛇身除外）到达食物的最短路径长；
（2）将蛇的安全定义为蛇是否可以跟着蛇尾运动，即蛇头和蛇尾间是否存在路径；
（3）蛇每次行动前先利用虚拟的蛇进行探路，若虚拟的蛇吃完食物后是安全的，真蛇才行动；
（4）若蛇和食物之间不存在路径或者吃完食物后并不安全，就跟着蛇尾走；
（5）若蛇和食物之间、蛇和蛇尾之间均不存在路径，就随便挑一步可行的来走；
（6）保证目标是食物时蛇走最短路径，目标是蛇尾时蛇走最长路径。
"""

pygame.init() # 初始化pygame
swidth = 1000
sheight = 800
screen = pygame.display.set_mode((swidth,sheight)) # 设置窗口大小(1000,800)
color = (255,255,255) # 白色方块
bgcolor = (0,0,0) # 黑色背景
running = True
x = 100 # 方块x坐标
y = 100 # 方块y坐标
timer = pygame.time.Clock() # 动画定时器
direction = 'right'
size = 50
applex = 300
appley = 100
apple_img = pygame.image.load("apple.png").convert_alpha()
apple_img = pygame.transform.scale(apple_img, (size, size))
sound = pygame.mixer.Sound("eaten.wav")
body = [(x,y)]
score = 0
font = pygame.font.SysFont('arial',54) # 设置字体
boardw = int(swidth/size)
boardh = int(sheight/size)
g_board = [[0]*boardh for i in range(boardw)] # 用0初始化背板
# 运动方向字典
move = {
    'up':(0,-1),
    'down':(0,1),
    'left':(-1,0),
    'right':(1,0),
}
# 不同东西在矩阵里用不同的数字表示
APPLE_PLACE = 0
FREE_PLACE = boardw*boardh + 1
SNAKE_PLACE = FREE_PLACE*2


def reset_board(board, snake, apple):
    """重置board，标记每个格子存储什么元素"""
    for x in range(boardw):
        for y in range(boardh):
            if x*size == apple[0] and y*size == apple[1]:
                board[x][y] = APPLE_PLACE
            elif (x*size,y*size) in snake:
                board[x][y] = SNAKE_PLACE
            else:
                board[x][y] = FREE_PLACE
    return
    

def bfs_board(board, snake, apple):
    """广度优先搜索遍历整个board.
    计算出board中每个非SNAKE_PLACE元素到达食物的路径长度
    """
    queue = []
    queue.append((int(apple[0]/size), int(apple[1]/size)))
    inqueue = [[0]*boardh for i in range(boardw)]
    found = False
    while len(queue) != 0:
        pos = queue.pop(0)
        px = pos[0]
        py = pos[1]
        if inqueue[px][py] == 1:  # 已经遍历过，不用遍历
            continue
        inqueue[px][py] = 1
        for d in ['left', 'right', 'up', 'down']:
            newx = px + move[d][0]
            newy = py + move[d][1]
            if is_move_possible(pos, d):
                # 找到蛇头，标记true
                if (newx, newy) == (convert_to_pos(snake[0][0]), convert_to_pos(snake[0][1])): 
                    found = True
                # 如果该点不是蛇身，计算路径长度，加入queue
                if board[newx][newy] < SNAKE_PLACE:
                    if board[newx][newy] > board[px][py] + 1:  # 用最小路径覆盖
                        board[newx][newy] = board[px][py] + 1  # 路径长度+1
                    if inqueue[newx][newy] == 0:  # 如果未遍历过
                        queue.append((newx, newy))   # 加入新坐标到queue
    return found

def print_snake(snake):
    ns = [(convert_to_pos(it[0]), convert_to_pos(it[1])) for it in snake]
    print(ns)

def get_snake(snake):
    ns = [(convert_to_pos(it[0]), convert_to_pos(it[1])) for it in snake]
    return ns


def print_board(board):
    for y in range(boardh):
        s = ''
        for x in range(boardw):
            s += str(board[x][y]) + ' '
        print(s)


def is_move_possible(pos, direction):
    """检查位置pos是否可以向当前move方向运动"""
    px = pos[0]
    py = pos[1]
    newx = px + move[direction][0]
    newy = py + move[direction][1]
    
    if newx < 0:
        return False
    if newx >= boardw:
        return False
    if newy < 0:
        return False
    if newy >= boardh:
        return False
    return True


def find_safe_way(board, snake, apple):
    """如果蛇和食物间有路径,则需要找一条安全的路径"""
    safe_move = -1
    real_board = copy.deepcopy(board)
    real_snake = copy.deepcopy(snake)
    v_board, v_snake = virtual_move(board, snake, apple)
    # 如果虚拟运行后，蛇头蛇尾间有通路，则选最短路运行
    if can_reach_tail(v_board, v_snake, apple):
        safe_move = choose_shortest_safe_move(real_board, real_snake)
        #print("snake",get_snake(real_snake),"safe_move:",safe_move)
    else:
        #print("follow_tail")
        safe_move = follow_tail(real_board, real_snake, apple)
    return safe_move


def virtual_move(board, snake, apple):
    """用虚拟的蛇进行探路"""
    temp_snake = copy.deepcopy(snake)
    temp_board = copy.deepcopy(board)
    reset_board(temp_board, temp_snake, apple)  # 重置board
    food_eated = False
    while not food_eated:
        bfs_board(temp_board, temp_snake, apple) # 计算board每个格子到苹果的最短路径
        move_direction = choose_shortest_safe_move(temp_board, temp_snake)  # 选择最短路径的移动方向
        #snake_Coords = temp_snake[:]
        temp_snake.insert(0, find_snake_head_cordinate(temp_snake, move_direction))  # 蛇走一步，插入新蛇头
        # 如果新的蛇头正好是食物的位置
        if temp_snake[0] == apple:
            reset_board(temp_board, temp_snake, apple)  # 重置board
            temp_board[convert_to_pos(apple[0])][convert_to_pos(apple[1])] = SNAKE_PLACE  # 虚拟蛇占领这个位置
            food_eated = True
        else:
            newheadposx = convert_to_pos(temp_snake[0][0])
            newheadposy = convert_to_pos(temp_snake[0][1])
            temp_board[newheadposx][newheadposy] = SNAKE_PLACE # 虚拟蛇头占领这个位置	
            tailx = convert_to_pos(temp_snake[-1][0])
            taily = convert_to_pos(temp_snake[-1][1])
            temp_board[tailx][taily] = FREE_PLACE # 释放蛇尾位置
            temp_snake.pop() # 删除蛇尾
    return temp_board, temp_snake


def convert_to_pos(x):
    return int(x/size)


def choose_shortest_safe_move(board, snake):
    """根据board中元素值, 从蛇头周围4个领域点中选择最短路径"""
    best_move = -1  # 没有结果
    min_distance = SNAKE_PLACE # 初始化一个很大很大的数
    snake_head_pos = (convert_to_pos(snake[0][0]), convert_to_pos(snake[0][1]))
    for d in ['left', 'right', 'up', 'down']:
        newx = snake_head_pos[0] + move[d][0]
        newy = snake_head_pos[1] + move[d][1]
        if is_move_possible(snake_head_pos, d) and board[newx][newy] < min_distance:
            min_distance = board[newx][newy]
            best_move = d
    """
    if best_move == -1:
        for d in ['left', 'right', 'up', 'down']:
            newx = snake_head_pos[0] + move[d][0]
            newy = snake_head_pos[1] + move[d][1]
            if is_move_possible(snake_head_pos, d) and board[newx][newy] < min_distance and board[newx][newy] >=0:
                min_distance = board[newx][newy]
                best_move = d
            print("d:%s,best_move:%s,snake_head_pos:%s,is_move_possible(snake_head_pos, d):%s,board[%s][%s]:%s" % (
                d,best_move,snake_head_pos,is_move_possible(snake_head_pos, d),newx,newy,board[newx][newy]))
        print(snake_head_pos)
        print_board(board)
        print(best_move)
    """
    return best_move


def find_snake_head_cordinate(snake, direction):
    """找到移动后蛇头的位置"""
    return (snake[0][0] + move[direction][0]*size, snake[0][1] + move[direction][1]*size)


def can_reach_tail(board, snake, apple):
    """检查蛇头和蛇尾间是有路径的, 避免蛇陷入死路"""
    temp_board = copy.deepcopy(board)
    temp_snake = copy.deepcopy(snake)
    # 将蛇尾看作食物
    tailx = convert_to_pos(temp_snake[-1][0])
    taily = convert_to_pos(temp_snake[-1][1])
    temp_board[tailx][taily] = APPLE_PLACE
    v_apple = temp_snake[-1]
    # 食物看作蛇身(重复赋值了)
    ax = convert_to_pos(apple[0])
    ay = convert_to_pos(apple[1])
    temp_board[ax][ay] = SNAKE_PLACE
    # 求得每个位置到蛇尾的路径长度
    result = bfs_board(temp_board, temp_snake, v_apple)
    """
    for d in ['left', 'right', 'up', 'down']:
        snake_head_pos = (convert_to_pos(temp_snake[0][0]), convert_to_pos(temp_snake[0][1]))
        snake_tail_pos = (convert_to_pos(temp_snake[-1][0]), convert_to_pos(temp_snake[-1][1]))
        if is_move_possible(snake_head_pos, d) and (snake_head_pos[0]+move[d][0], snake_head_pos[1]+move[d][1]) == snake_tail_pos and (len(temp_snake)>3):
            result = False
    """
    return result


def follow_tail(board, snake, apple):
    """让蛇头朝着蛇尾运行一步"""
    temp_snake = copy.deepcopy(snake)
    temp_board = copy.deepcopy(board)
    reset_board(temp_board, temp_snake, apple)
    
    # 将蛇尾看作食物
    tailx = convert_to_pos(temp_snake[-1][0])
    taily = convert_to_pos(temp_snake[-1][1])
    temp_board[tailx][taily] = APPLE_PLACE
    v_apple = temp_snake[-1]
    # 食物看作蛇身(重复赋值了)
    ax = convert_to_pos(apple[0])
    ay = convert_to_pos(apple[1])
    temp_board[ax][ay] = SNAKE_PLACE
    # 求得每个位置到蛇尾的路径长度
    result = bfs_board(temp_board, temp_snake, v_apple)
    # 还原
    temp_board[tailx][taily] = SNAKE_PLACE
    #temp_board[ax][ay] = APPLE_PLACE
    return choose_longest_safe_move(temp_board, temp_snake)


def choose_longest_safe_move(board, snake):
    """根据board中元素值,从蛇头周围4个领域点中选择最远路径"""
    best_move = -1
    max_distance = -1
    snake_head_pos = (convert_to_pos(snake[0][0]), convert_to_pos(snake[0][1]))
    for d in ['left', 'right', 'up', 'down']:
        newx = snake_head_pos[0] + move[d][0]
        newy = snake_head_pos[1] + move[d][1]
        if is_move_possible(snake_head_pos, d) and board[newx][newy] > max_distance and board[newx][newy] < FREE_PLACE:
            max_distance = board[newx][newy]
            best_move = d
    return best_move


def any_possible_move(board, snake, apple):
    """各种方案均无效时，随便走一步"""
    best_move = -1  # 没有结果
    reset_board(board, snake, apple)
    result = bfs_board(board, snake, apple)
    min_distance = SNAKE_PLACE # 初始化一个很大很大的数
    for d in ['left', 'right', 'up', 'down']:
        snake_head_pos = (convert_to_pos(snake[0][0]), convert_to_pos(snake[0][1]))
        newx = snake_head_pos[0] + move[d][0]
        newy = snake_head_pos[1] + move[d][1]
        if is_move_possible(snake_head_pos, d) and board[newx][newy] < min_distance:
            min_distance = board[newx][newy]
            best_move = d
    return best_move


def show_score():
    score_words = font.render('AI SCORE:'+str(score), True, (0,255,0))
    screen.blit(score_words, [20,20])

def gameover():
    go_words = font.render('GAME OVER!', True, (0,255,0)) #游戏结束内容显示
    screen.blit(go_words, [400,300])
    score_words = font.render('SCORE:'+str(score), True, (0,255,0))
    screen.blit(score_words, [400,400])
    pygame.display.update() # 刷新整个画布

    
def check_eaten():
    if applex == x and appley == y:
        return True
    else:
        return False

def draw_snake():
    for i,pos in enumerate(body):
        if i==0:
            scolor = (255,255,0)
        elif i==len(body)-1:
            scolor = (0,255,255)
        else:
            scolor = color
        pygame.draw.rect(screen, scolor, pygame.Rect(pos[0],pos[1],size,size)) # 画方块Rect(x坐标，y坐标，宽度，高度)

def check_gameover():
    if x >= swidth or x < 0 or y >= sheight or y < 0:
        return True
    for pos in body[1:]:
        if x == pos[0] and y == pos[1]:
            return True
    return False

def new_apple():
    """生成一个新的苹果,不能与蛇重叠。"""
    while True:
        ax = random.randint(0, boardw-1) * size
        ay = random.randint(0, boardh-1) * size
        if (ax, ay) not in body:
            break
    return (ax, ay)
        
    
while running:
    # 获取所有玩家事件
    for event in pygame.event.get():
        # 如果是关闭窗口事件，那么退出循环
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
            elif event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'
            elif event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
            elif event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'

    if check_gameover():
        gameover()
        continue  # 流程中止，继续下一次循环
    
    # 重置board
    # 计算bfs最短路径
    applepos = (applex,appley)
    reset_board(g_board, body, applepos)
    
    #print_snake(body)
    #print_board(g_board)
    
    can_eat = bfs_board(g_board, body, applepos)
    #print_board(board)
    if can_eat: # 可以吃到苹果
        best_move = find_safe_way(g_board, body, applepos)
        #print("find_safe_way: best_move:%s, (%s,%s)" % (best_move, x, y))
    else:
        #print("follow_tail")
        best_move = follow_tail(g_board, body, applepos)
    if best_move == -1:  # 都不满足，随便走走
        print("wander walk")
        best_move = any_possible_move(g_board, body, applepos)
    if best_move != -1:
        # 开始移动
        newhead = find_snake_head_cordinate(body, best_move)
        x = newhead[0]
        y = newhead[1]
    else:
        # 最终没有路径的话，向右走
        print("no way, walk right")
        x = x + size
        newhead = (x, y)
    body.insert(0, newhead)

    if check_eaten():
        # 播放声音
        sound.play()
        # 生成一个新的苹果
        applex, appley = new_apple()
        # 分数+1
        score += 1
    else:
        body.pop() # 删除最后一段

    
    screen.fill(bgcolor) # 清除整个画布
    draw_snake() # 画蛇
    screen.blit(apple_img, (applex,appley)) # 画苹果
    show_score() # 展示分数
    pygame.display.update() # 刷新整个画布
    timer.tick(100)  # 帧速率，控制刷新速度

pygame.quit() # 退出关闭窗口




