import pygame
import os

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

music_folder = "musics"
music_files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
current_track = 0

pygame.mixer.init()
if music_files:
    pygame.mixer.music.load(os.path.join(music_folder, music_files[current_track]))


def play_music():
    pygame.mixer.music.play()


def stop_music():
    pygame.mixer.music.stop()


def next_track():
    global current_track
    current_track = (current_track + 1) % len(music_files)
    pygame.mixer.music.load(os.path.join(music_folder, music_files[current_track]))
    play_music()


def previous_track():
    global current_track
    current_track = (current_track - 1) % len(music_files)
    pygame.mixer.music.load(os.path.join(music_folder, music_files[current_track]))
    play_music()


isRun = True

while isRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRun = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        play_music()
    if keys[pygame.K_DOWN]:
        stop_music()
    if keys[pygame.K_RIGHT]:
        next_track()
    if keys[pygame.K_LEFT]:
        previous_track()

    screen.fill((255, 255, 255))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
