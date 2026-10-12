import pygame
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

pygame.init()

screen = pygame.display.set_mode((400, 600))

running = True
clock = pygame.time.Clock()

speed = 300  
bullet_speed = 500
player_image = pygame.image.load(str(BASE_DIR / "plane.png")).convert_alpha()
player_image = pygame.transform.scale(player_image, (80, 80))
player_mask = pygame.mask.from_surface(player_image)
enemy_image = pygame.image.load(str(BASE_DIR / "enemy.png")).convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50,50))
enemy_image = pygame.transform.rotate(enemy_image, 180)
enemy_mask = pygame.mask.from_surface(enemy_image)
bullet_mask = pygame.mask.Mask((5,10), fill= True)
player_pos = pygame.Vector2(150, 425) 
bullets = []
shoot_delay = 200
last_shot_time = 0
enemies = []
enemy = pygame.Rect(150, -50, 50 ,50)
enemies.append(enemy)
enemy_speed = 100
score = 0
font = pygame.font.Font(None, 36)
game_over = False

while running:
     
    dt= clock.tick(60)/ 1000 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = False
                score = 0
                enemy_speed = 100
                player_pos = pygame.Vector2(150, 425)
                bullets.clear()
                enemies.clear()
                enemy = pygame.Rect(random.randint(0,350), -50, 50, 50)
                enemies.append(enemy)
    if not game_over:
        for enemy in enemies:
            enemy.y +=enemy_speed * dt
            if enemy.top > 600:
                enemy.y = -50
                enemy.x = random.randint(0,350)

        for bullet in bullets.copy():
            bullet.y -= bullet_speed * dt
            hit_enemy = False
            for enemy in enemies:
                offset = (bullet.x - enemy.x, bullet.y - enemy.y)
                if enemy_mask.overlap(bullet_mask, offset):
                    bullets.remove(bullet)
                    score += 1

                    enemy.y = -50
                    enemy.x = random.randint(0,350)

                    hit_enemy = True
                    break
            if not hit_enemy and bullet.bottom < 0:
                bullets.remove(bullet)

        enemy_speed = min(100 + score * 5, 375)
        enemy_count = min(1 + score // 5, 20)
        while len(enemies) < enemy_count:
            enemy = pygame.Rect(random.randint(0,350), random.randint(-200,-50), 50, 50)
            enemies.append(enemy)

    
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_SPACE]:
            if current_time - last_shot_time > shoot_delay:
                bullet = pygame.Rect(player_pos.x + 37, player_pos.y, 5, 10)
                bullets.append(bullet)
                last_shot_time = current_time

        if keys[pygame.K_a]:
            direction.x -= 1

        if keys[pygame.K_d]:
            direction.x += 1

        if keys[pygame.K_w]:
            direction.y -= 1

        if keys[pygame.K_s]:
            direction.y += 1
        if direction.length() > 0:
            direction = direction.normalize()
        player_pos += direction * speed * dt

    
        player_pos.x = min(player_pos.x, 320) 
        player_pos.x = max(player_pos.x, 0) 
        player_pos.y = min(player_pos.y, 520) 
        player_pos.y = max(player_pos.y, 0) 
        player_rect = pygame.Rect(player_pos.x, player_pos.y, 80, 80)
        for enemy in enemies:
            offset = (enemy.x - int(player_pos.x), enemy.y - int(player_pos.y))
            if player_mask.overlap(enemy_mask, offset):
                game_over = True

    screen.fill((0, 0, 0))

    screen.blit(player_image, player_pos)
    for enemy in enemies:
        screen.blit(enemy_image, enemy)
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)

    score_text = font.render(f"Score {score}", True, (255,255,255))
    screen.blit(score_text,(10,10))

    if game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (150, 300))
        restart_text = font.render("Press R to restart", True, (255,255,255))
        screen.blit(restart_text, (100, 340))

    pygame.display.flip()

pygame.quit()
