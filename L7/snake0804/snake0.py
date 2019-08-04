import pygame
import random

# 游戏初始化
pygame.init() # 初始化pygame
screen = pygame.display.set_mode((1000,800)) # 设置窗口大小(1000,800)
color = (255,255,255) # 白色方块
bgcolor = (0,0,0) # 黑色背景
running = True
x = 100 # 蛇头x坐标
y = 100 # 蛇头y坐标
timer = pygame.time.Clock() # 动画定时器
size = 50  # 方块大小
direction = 'right'  # 蛇的运动方向
apple_img = pygame.image.load('10.jpeg').convert_alpha()
apple_img = pygame.transform.scale(apple_img, (size,size))  # 苹果图像
applex = 300 # 苹果x坐标
appley = 100 # 苹果y坐标
sound = pygame.mixer.Sound('eaten.wav')  # 加载声音文件
body = [(x,y)] # 蛇的身体，数组类型，包含了所有组成蛇的方块坐标
font = pygame.font.SysFont('arial', 54)  # 字体
score = 0 # 分数


def show_score():
    """展示分数"""
    scoreword = font.render('SCORE:' + str(score), True, (255,255,255))
    screen.blit(scoreword, (20,20))

    
def show_gameover():
    """展示game over"""
    goword = font.render('GAMEOVER', True, (0,255,0))
    screen.blit(goword, (400,400))
    pygame.display.update()  # 刷新屏幕
    

def check_gameover():
    """检查是否游戏结束。
    1 检查蛇头是否碰到了屏幕边界
    2 检查蛇头是否碰到了自己的身体
    """
    if x < 0 or x >= 1000 or y < 0 or y >= 800:
        return True
    for cor in body[1:]:  # body[1:]表示从数组第二个元素开始循环，不包含第一个元素(蛇头)
        if x == cor[0] and y == cor[1]:
            return True
    return False


def draw_snake():
    """画蛇"""
    for pos in body:
        pygame.draw.rect(screen, color,
            pygame.Rect(pos[0],pos[1],50,50)) # 画方块Rect(x坐标，y坐标，宽度，高度)

    
def check_eaten():
    """检查是吃到了苹果"""
    if x == applex and y == appley:
        return True
    else:
        return False


# 游戏主循环
while running:
    # 获取所有玩家事件
    for event in pygame.event.get():
        # 如果是关闭窗口事件，那么退出循环
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = 'up'
            elif event.key == pygame.K_DOWN:
                direction = 'down'
            elif event.key == pygame.K_LEFT:
                direction = 'left'
            elif event.key == pygame.K_RIGHT:
                direction = 'right'
                
    # 判断游戏结束
    # 如果游戏结束，展示gameover文字
    if check_gameover():  
        show_gameover()
        continue 

    # 控制蛇的方向
    if direction == 'up':
        y = y - size
    elif direction == 'down':
        y = y + size
    elif direction == 'left':
        x = x - size
    elif direction == 'right':
        x = x + size
    body.insert(0, (x,y))

    # 检查是否吃到了苹果
    if check_eaten():
        sound.play() # 播放声音
        score += 1 # 分数+1
        # 生成新苹果
        applex = random.randint(0, 1000/size-1)*size
        appley = random.randint(0, 800/size-1)*size
    else:
        body.pop() # 删除尾部
        
    screen.fill(bgcolor) # 清除整个画布
    draw_snake() # 画蛇
    show_score() # 展示分数
    screen.blit(apple_img, (applex, appley)) # 画苹果
    pygame.display.update() # 刷新整个画布
    timer.tick(10)  # 帧速率，控制刷新速度

pygame.quit()  # 游戏退出


