# Music Visualizer

This project is about building audio processing pipleline, extracts layers from the the audio and visualize them.

## Audio extraction

## Step 1:

The audio is preformed in a digital form so we used an algorithm called FFT (Fast Fourier transform) to transform the audio into signal wave, this is important for visualization.

## Step 2:

We got a list of numbers that can visualized but using this raw list will visualize the wave as static waves so I prefered to extract 3 layers from the audio.

1. Bass
2. Mids
3. Treble

Each of these layers has it own frequency range measuered in Hz, this helps for better visualization since we made each one work on it own.

## Visualization

It was vibe coded using DeepSeek nothing serious, can be modified as much playing around with numbers and add new effect based on your vision.

Pygame was used but there is better libraries can be merged with it to produce more good looking visualization like: "ModernGL" as an example.

of the audio and the visualization are synced together and the music run in the background with it own thread.

# How to use?

1. clone the repository.
2. make sure you got uv installed into your system.
3. use the command `uv sync` to sync all dependencines into a virtual env
4. add your own audio path and change the values of line 26 and 32:
    `pygame.mixer.music.load("youraudio.mp3")`
    `bass, mids, treble, sampleRate = extract_bands("youraudio.mp3")`

5. run the visualization using the command:
    `uv run visualization.py`