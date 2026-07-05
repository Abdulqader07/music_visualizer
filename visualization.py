import math
import pygame
import threading
import time
import numpy as np
import pygame.gfxdraw
from processing import extract_bands
from files import selectAudio

WIDTH = 1080
HEIGHT = 720

X_CENTER = WIDTH // 2
Y_CENTER = HEIGHT // 2
BASE_RADIUS = 150

# Gain controls
BASS_GAIN = 1.2      
MIDS_GAIN = 2.0      
TREBLE_GAIN = 3.3 

BACKGROUND_COLOR = (39, 36, 41)
CIRCLE_COLOR = (231, 200, 247)

audio_file = selectAudio()

if not audio_file:
    print('error no file')
    exit()

def playAudio():
    pygame.mixer.init(buffer=512)
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

pygame.init()

# Extract bands
bass, mids, treble, sampleRate = extract_bands(audio_file)
numFrames = len(bass)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Audio Visualizer")

# Smoothing
smooth_bass = 0
smooth_mids = 0
smooth_treble = 0
smooth_factor = 0.3

running = True
clock = pygame.time.Clock()

# Start audio and record time
audioThreading = threading.Thread(target=playAudio, daemon=True)
audio_start_time = time.time()
audioThreading.start()

# Time per frame (hop_length / sampleRate)
time_per_frame = 1024 / sampleRate

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # Calculate which frame should be showing based on audio time
    elapsed = time.time() - audio_start_time
    target_frame = int(elapsed / time_per_frame)
    
    if target_frame >= numFrames:
        target_frame = numFrames - 1

        # Auto-close after 3 seconds when song ends
    if target_frame >= numFrames - 1 and not pygame.mixer.music.get_busy():
        pygame.display.flip()
        pygame.time.wait(3000)  # 3 seconds
        running = False
        break
    
    if target_frame < 0:
        target_frame = 0
    
    frameIndex = target_frame

    # Get current frame values
    raw_bass = bass[frameIndex]
    raw_mids = mids[frameIndex]
    raw_treble = treble[frameIndex]
    
    # Apply gain
    bass_val = min(1.0, raw_bass * BASS_GAIN)
    mids_val = min(1.0, raw_mids * MIDS_GAIN)
    treble_val = min(1.0, raw_treble * TREBLE_GAIN)
    
    # Smoothing
    smooth_bass = smooth_bass + (bass_val - smooth_bass) * smooth_factor
    smooth_mids = smooth_mids + (mids_val - smooth_mids) * smooth_factor
    smooth_treble = smooth_treble + (treble_val - smooth_treble) * smooth_factor
    
    # Fixed circle
    circle_radius = BASE_RADIUS
    pygame.gfxdraw.aacircle(screen, X_CENTER, Y_CENTER, int(circle_radius), CIRCLE_COLOR)
    
    # Wave offsets (all push outward)
    bass_offset = smooth_bass * 60
    mids_offset = smooth_mids * 50
    treble_offset = smooth_treble * 40
    
    # Draw waves
    points_bass = []
    points_mids = []
    points_treble = []
    
    num_points = 60
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        
        # Bass wave (outer)
        bass_radius = circle_radius + bass_offset * (0.5 + 0.5 * math.sin(angle * 2))
        x_bass = X_CENTER + bass_radius * math.cos(angle)
        y_bass = Y_CENTER + bass_radius * math.sin(angle)
        points_bass.append((x_bass, y_bass))
        
        # Mids wave (outer)
        mids_radius = circle_radius + mids_offset * (0.5 + 0.5 * math.cos(angle * 3))
        x_mids = X_CENTER + mids_radius * math.cos(angle)
        y_mids = Y_CENTER + mids_radius * math.sin(angle)
        points_mids.append((x_mids, y_mids))
        
        # Treble wave (outer)
        treble_radius = circle_radius + treble_offset * (0.5 + 0.5 * math.sin(angle * 4 + 0.5))
        x_treble = X_CENTER + treble_radius * math.cos(angle)
        y_treble = Y_CENTER + treble_radius * math.sin(angle)
        points_treble.append((x_treble, y_treble))
    
    # Draw bass wave (blue)
    if len(points_bass) > 2:
        pygame.draw.lines(screen, (240, 19, 104), True, points_bass, 2)
        for point in points_bass[::3]:
            pygame.draw.circle(screen, (242, 34, 110), (int(point[0]), int(point[1])), 3)
    
    # Draw mids wave (green)
    if len(points_mids) > 2:
        pygame.draw.lines(screen, (245, 159, 191), True, points_mids, 2)
        for point in points_mids[::3]:
            pygame.draw.circle(screen, (245, 174, 200), (int(point[0]), int(point[1])), 3)
    
    # Draw treble wave (yellow)
    if len(points_treble) > 2:
        pygame.draw.lines(screen, (185, 73, 245), True, points_treble, 1)
        for point in points_treble[::3]:
            pygame.draw.circle(screen, (183, 93, 232), (int(point[0]), int(point[1])), 2)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()