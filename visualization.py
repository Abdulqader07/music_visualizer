import math
import pygame
import threading
import time
import numpy as np
import pygame.gfxdraw
from processing import extract_bands

WIDTH = 1080
HEIGHT = 720

X_CENTER = WIDTH // 2
Y_CENTER = HEIGHT // 2
BASE_RADIUS = 150

# Gain controls
BASS_GAIN = 1.2      
MIDS_GAIN = 2.0      
TREBLE_GAIN = 3.3 

BACKGROUND_COLOR = (10, 10, 20)
CIRCLE_COLOR = (100, 200, 255)

def playAudio():
    pygame.mixer.init(buffer=512)
    pygame.mixer.music.load("Yeat - Every month.mp3")
    pygame.mixer.music.play()

pygame.init()

# Extract bands

bass, mids, treble, sampleRate = extract_bands("Yeat - Every month.mp3")
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
    
    # Wave offsets
    wave_in_offset = smooth_bass * 60
    wave_out_offset = smooth_treble * 60
    
    # Draw waves
    points_in = []
    points_out = []
    points_mid = []
    
    num_points = 60
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        
        # Inner wave (bass)
        inner_radius = circle_radius + wave_in_offset * (0.5 + 0.5 * math.sin(angle * 2))
        x_in = X_CENTER + inner_radius * math.cos(angle)
        y_in = Y_CENTER + inner_radius * math.sin(angle)
        points_in.append((x_in, y_in))
        
        # Outer wave (treble)
        outer_radius = circle_radius + wave_out_offset * (0.5 + 0.5 * math.cos(angle * 3))
        x_out = X_CENTER + outer_radius * math.cos(angle)
        y_out = Y_CENTER + outer_radius * math.sin(angle)
        points_out.append((x_out, y_out))
        
        # Mid wave (mids)
        mid_radius = circle_radius + (smooth_mids * 40) * math.sin(angle * 4)
        x_mid = X_CENTER + mid_radius * math.cos(angle)
        y_mid = Y_CENTER + mid_radius * math.sin(angle)
        points_mid.append((x_mid, y_mid))
    
    # Draw waves
    if len(points_in) > 2:
        pygame.draw.lines(screen, (100, 150, 255), True, points_in, 2)
        for point in points_in[::3]:
            pygame.draw.circle(screen, (100, 150, 255), (int(point[0]), int(point[1])), 3)
    if len(points_out) > 2:
        pygame.draw.lines(screen, (255, 200, 100), True, points_out, 2)
        for point in points_out[::3]:
            pygame.draw.circle(screen, (255, 200, 100), (int(point[0]), int(point[1])), 3)
    
    if len(points_mid) > 2:
        pygame.draw.lines(screen, (100, 255, 150), True, points_mid, 1)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()