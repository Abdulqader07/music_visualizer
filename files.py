import tkinter as tk
from tkinter import filedialog

def selectAudio():
    root = tk.Tk()
    root.withdraw() # Hide the main window

    root.attributes('-topmost', True) # Bring to front

    audio_file = filedialog.askopenfilename(
        title = "Select your music file",
        filetypes= [
            ("Audio files", "*.mp3 *.wav *.ogg *.flac *.m4a"),
            ("Mp3 files", "*.mp3"),
            ("Wav files", "*.wav"),
            ("All files", "*.*")
        ]
    )

    root.destroy()

    return audio_file
