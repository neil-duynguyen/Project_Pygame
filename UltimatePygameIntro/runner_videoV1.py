import pygame
from sys import exit
from random import randint
from datetime import datetime
import json
import os

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def display_score(score):
    if score is None:
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
        score_rec = score_surf.get_rect(center = (400, 50))
        screen.blit(score_surf, score_rec)
        return current_time
    else:
        current_time = int(pygame.time.get_ticks() / 1000) - start_time + score
        score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
        score_rec = score_surf.get_rect(center = (400, 50))
        screen.blit(score_surf, score_rec)
        return current_time

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):

                # Tính toán thời gian kết thúc
                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # Lưu điểm và thời gian kết thúc vào file JSON
                save_score(score, end_time)
                return False

    return True

def save_score(score, end_time, folder_path='scores'):
    # Đảm bảo thư mục tồn tại
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Tạo đường dẫn đầy đủ cho file JSON
    file_path = os.path.join(folder_path, 'highscore.json')
    
    # Tạo dữ liệu để lưu vào JSON
    data = {
        'score': score,
        'end_time': end_time
    }
    
    try:
        # Kiểm tra nếu file đã tồn tại, đọc dữ liệu cũ
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                try:
                    existing_data = json.load(file)
                    if not isinstance(existing_data, list):
                        existing_data = []
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
        
        # Thêm dữ liệu mới vào danh sách
        existing_data.append(data)
        
        # Ghi dữ liệu mới vào file JSON
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)
        
        print("Score saved successfully!")

    except IOError as e:
        print(f"Error saving score: {e}")

def load_latest_score(folder_path='scores'):
    file_path = os.path.join(folder_path, 'highscore.json')

    if not os.path.exists(file_path):
        return None, None  # Không có dữ liệu

    try:
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
                if not existing_data:
                    return None, None  # File rỗng
                # Lấy bản ghi mới nhất
                latest_record = existing_data[-1]
                return latest_record['score'], latest_record['end_time']
            except json.JSONDecodeError:
                return None, None  # Lỗi phân tích JSON
    except IOError as e:
        print(f"Error reading score: {e}")
        return None, None

def player_animation():
    global player_surf, player_index
    # play walking animation if the player is on floor
    # display the jump surface when player is not a floor
    if player_rec.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf  = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock() # quản lý tốc độ khung hình
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_Music = pygame.mixer.Sound('audio/music.wav')
bg_Music.set_volume(0.5)
bg_Music.play()
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.5)
obstacle_rect_list = []

# Load backgound
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Player
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]

# Snail
snail_fram_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_fram_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_fram_1, snail_fram_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_fram_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_fram_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_fram_1, fly_fram_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# Jump
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rec = player_surf.get_rect(midbottom  = (80, 300))
player_gravity = 0


player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rec = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('Pixel Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_mess = test_font.render('Press space to run', False, (111,196,169))
game_mess_rect = game_mess.get_rect(center = (400, 340))


#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT = 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rec.bottom >= 300:
                    player_gravity =- 20
                    jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0 ,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100  ), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:

        # Đọc điểm số và thời gian lưu mới nhất khi khởi động trò chơi
        latest_score, latest_end_time = load_latest_score()

        # Nếu có dữ liệu, tiếp tục trò chơi với điểm số đó
        if latest_score is not None:
            load_score = latest_score
        else:
            load_score = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_w]:
            pygame.quit()
            exit()

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface, (0, 300))
        score = display_score(load_score)
    
        # Player 
        player_gravity += 1
        player_rec.y += player_gravity
        if player_rec.bottom >= 300 : player_rec.bottom = 300
        screen.blit(player_surf, player_rec)

        player_animation() 

        # Obstactle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collisions(player_rec, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rec)

        obstacle_rect_list.clear()
        player_rec.midbottom = (80,300)
        player_gravity = 0

        score_mess = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_mess_rect = score_mess.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_mess, game_mess_rect)
        else:
            screen.blit(score_mess, score_mess_rect)

    pygame.display.update()  
    clock.tick(60)