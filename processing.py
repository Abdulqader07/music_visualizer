import numpy as np
import soundfile as sf

def extract_bands(audio_file, chunk_size=2048, hop_length=1024):

    # Load audio
    data, sr = sf.read(audio_file, dtype='float32')
    
    # Convert to mono
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    
    # Process in chunks
    bass_list, mids_list,treble_list = [], [], []
    
    for i in range(0, len(data) - chunk_size, hop_length):
        chunk = data[i:i + chunk_size]
        
        # Apply window
        window = np.hanning(chunk_size)
        chunk = chunk * window
        
        fft = np.abs(np.fft.rfft(chunk))
        freqs = np.fft.rfftfreq(chunk_size, 1/sr)
        
        # Define frequency bands (Hz)
        bass_range = (20, 250)
        mids_range = (250, 4000)
        treble_range = (4000, 20000)
        
        # Get indices for each band
        bass_idx = np.where((freqs >= bass_range[0]) & (freqs < bass_range[1]))[0]
        mids_idx = np.where((freqs >= mids_range[0]) & (freqs < mids_range[1]))[0]
        treble_idx = np.where((freqs >= treble_range[0]) & (freqs < treble_range[1]))[0]
        
        # Calculate energy in each band
        bass_energy = np.mean(fft[bass_idx]) if len(bass_idx) > 0 else 0
        mids_energy = np.mean(fft[mids_idx]) if len(mids_idx) > 0 else 0
        treble_energy = np.mean(fft[treble_idx]) if len(treble_idx) > 0 else 0
        
        bass_list.append(bass_energy)
        mids_list.append(mids_energy)
        treble_list.append(treble_energy)
    
    # Convert to numpy arrays
    bass = np.array(bass_list)
    mids = np.array(mids_list)
    treble = np.array(treble_list)
    
    # Normalize each band to 0-1
    bass = (bass - np.min(bass)) / (np.max(bass) - np.min(bass) + 1e-10)
    mids = (mids - np.min(mids)) / (np.max(mids) - np.min(mids) + 1e-10)
    treble = (treble - np.min(treble)) / (np.max(treble) - np.min(treble) + 1e-10)
    
    return bass, mids, treble, sr
