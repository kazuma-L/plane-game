import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

running = True
clock = pygame.time.Clock()

speed = 300  # 每秒移动的像素数
player_pos = pygame.Vector2(100,100)  # 玩家初始位置
player = pygame.Rect(0, 0, 50, 50)  # 玩家矩形

while running:
     # 1. 限制 FPS
    dt= clock.tick(60)/ 1000 # 获取 deltaTime

    # 2. 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. 检查键盘
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_pos.x -= speed * dt

    if keys[pygame.K_RIGHT]:
        player_pos.x += speed * dt

    if keys[pygame.K_UP]:
        player_pos.y -= speed * dt

    if keys[pygame.K_DOWN]:
        player_pos.y += speed * dt

    # 4. 屏幕边界
    player_pos.x = min(player_pos.x, 775) # 右边界
    player_pos.x = max(player_pos.x, 25) # 左边界
    player_pos.y = min(player_pos.y, 575) # 下边界
    player_pos.y = max(player_pos.y,25) # 上边界

    # 5. 绘制
    player.center = player_pos  # 更新玩家矩形位置
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 0, 0), player)

    pygame.display.flip()

pygame.quit()
