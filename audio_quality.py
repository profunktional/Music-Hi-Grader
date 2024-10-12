import os
import wave
import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.aiff import AIFF
from pydub import AudioSegment

SUPPORTED_FORMATS = ('.wav', '.aiff', '.flac', '.alac', '.wma', '.ape', '.wv', '.tta', '.mp4', '.m4a', '.mp3', '.aac', '.ogg', '.opus', '.mpc', '.atrac')

def check_file_integrity(file_path):
    try:
        if file_path.lower().endswith('.wav'):
            with wave.open(file_path, 'rb') as audio:
                audio.readframes(audio.getnframes())
        elif file_path.lower().endswith('.aiff'):
            audio = AIFF(file_path)
        elif file_path.lower().endswith('.flac'):
            audio = FLAC(file_path)
        elif file_path.lower().endswith(('.alac', '.m4a', '.mp4')):
            audio = MP4(file_path)
        elif file_path.lower().endswith('.wma'):
            audio = mutagen.File(file_path)
        elif file_path.lower().endswith('.ape'):
            audio = mutagen.File(file_path)
        elif file_path.lower().endswith('.wv'):
            audio = mutagen.File(file_path)
        elif file_path.lower().endswith('.tta'):
            audio = mutagen.File(file_path)
        elif file_path.lower().endswith('.mp3'):
            audio = MP3(file_path)
        elif file_path.lower().endswith('.aac'):
            audio = MP4(file_path)
        elif file_path.lower().endswith('.ogg'):
            audio = OggVorbis(file_path)
        elif file_path.lower().endswith('.opus'):
            audio = mutagen.File(file_path)
        elif file_path.lower().endswith('.mpc'):
            audio = mutagen.File(file_path)
        elif file_path.lower().endswith('.atrac'):
            audio = mutagen.File(file_path)
        else:
            return False
        return True
    except Exception as e:
        print(f"File integrity check failed for {file_path}: {e}")
        return False

def get_uncompressed_quality(file_path):
    try:
        with wave.open(file_path, 'rb') as audio:
            sample_rate = audio.getframerate()
            bit_depth = audio.getsampwidth() * 8
            channels = audio.getnchannels()
            return {
                'sample_rate': sample_rate,
                'bit_depth': bit_depth,
                'channels': channels
            }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def get_lossless_quality(file_path):
    try:
        if file_path.endswith('.flac'):
            audio = FLAC(file_path)
        elif file_path.endswith('.alac') or file_path.endswith('.m4a'):
            audio = MP4(file_path)
        elif file_path.endswith('.wma'):
            audio = mutagen.File(file_path)
        elif file_path.endswith('.ape'):
            audio = mutagen.File(file_path)
        elif file_path.endswith('.wv'):
            audio = mutagen.File(file_path)
        elif file_path.endswith('.tta'):
            audio = mutagen.File(file_path)
        else:
            return None
        
        sample_rate = audio.info.sample_rate
        bit_depth = audio.info.bits_per_sample
        channels = audio.info.channels
        return {
            'sample_rate': sample_rate,
            'bit_depth': bit_depth,
            'channels': channels
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def get_lossy_quality(file_path):
    try:
        if file_path.endswith('.mp3'):
            audio = MP3(file_path)
        elif file_path.endswith('.aac') or file_path.endswith('.m4a'):
            audio = MP4(file_path)
        elif file_path.endswith('.ogg'):
            audio = OggVorbis(file_path)
        elif file_path.endswith('.opus'):
            audio = mutagen.File(file_path)
        elif file_path.endswith('.mpc'):
            audio = mutagen.File(file_path)
        elif file_path.endswith('.atrac'):
            audio = mutagen.File(file_path)
        else:
            return None
        
        bitrate = audio.info.bitrate
        sample_rate = audio.info.sample_rate
        channels = audio.info.channels
        return {
            'bitrate': bitrate,
            'sample_rate': sample_rate,
            'channels': channels
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def get_audio_quality(file_path):
    if not check_file_integrity(file_path):
        print(f"File {file_path} is corrupted or incomplete.")
        return None

    if file_path.lower().endswith(('.wav', '.aiff', '.pcm', '.bwf')):
        return get_uncompressed_quality(file_path)
    elif file_path.lower().endswith(('.flac', '.alac', '.wma', '.ape', '.wv', '.tta', '.m4a', '.mp4')):
        return get_lossless_quality(file_path)
    elif file_path.lower().endswith(('.mp3', '.aac', '.ogg', '.opus', '.mpc', '.atrac')):
        return get_lossy_quality(file_path)
    else:
        return None

# Example usage
file_path = 'path/to/your/audio/file'
quality = get_audio_quality(file_path)
if quality:
    for key, value in quality.items():
        print(f"{key.capitalize()}: {value}")
else:
    print("Unsupported file format or error processing the file.")
