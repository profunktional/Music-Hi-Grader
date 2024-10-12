import os
import filetype
from pydub import AudioSegment
from mutagen import File

def detect_audio_file_type(file_path):
    kind = filetype.guess(file_path)
    if kind is None:
        return "Unknown"
    return kind.mime

def get_audio_details(file_path):
    file_type = detect_audio_file_type(file_path)
    print(f"File Type: {file_type}")
    
    if "audio" not in file_type:
        print("Not an audio file.")
        return
    
    audio = AudioSegment.from_file(file_path)
    
    duration = len(audio) / 1000.0  # Duration in seconds
    channels = audio.channels
    frame_rate = audio.frame_rate
    sample_width = audio.sample_width
    file_size = os.path.getsize(file_path)  # File size in bytes
    bit_depth = sample_width * 8  # Bit depth in bits
    bitrate = (file_size * 8) / duration  # Bitrate in bits per second
    
    audio_file = File(file_path)
    metadata = audio_file.tags
    
    print(f"File: {file_path}")
    print(f"Duration: {duration} seconds")
    print(f"Channels: {channels}")
    print(f"Frame Rate: {frame_rate} Hz")
    print(f"Sample Width: {sample_width} bytes")
    print(f"File Size: {file_size} bytes")
    print(f"Bit Depth: {bit_depth} bits")
    print(f"Bitrate: {bitrate} bits per second")
    #print(f"Metadata: {metadata}")
    print("-" * 40)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            get_audio_details(file_path)

# Example usage
directory_path = "samples/"
process_directory(directory_path)