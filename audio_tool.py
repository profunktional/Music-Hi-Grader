import os
import wave
import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.aiff import AIFF
from pydub import AudioSegment
import shutil

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

def get_audio_metadata(file_path):
    try:
        audio = mutagen.File(file_path, easy=True)
        if audio is None or not audio.tags:
            return None
        title = audio.get('title', [None])[0]
        artist = audio.get('artist', [None])[0]
        if not title or not artist:
            return None
        return {
            'title': title,
            'artist': artist,
            'album': audio.get('album', [None])[0],
            'format': file_path.split('.')[-1]
        }
    except Exception as e:
        print(f"Metadata check failed for {file_path}: {e}")
        return None

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

    metadata = get_audio_metadata(file_path)
    if not metadata:
        print(f"File {file_path} is missing metadata.")
        return None

    if file_path.lower().endswith(('.wav', '.aiff', '.pcm', '.bwf')):
        quality = get_uncompressed_quality(file_path)
    elif file_path.lower().endswith(('.flac', '.alac', '.wma', '.ape', '.wv', '.tta', '.m4a', '.mp4')):
        quality = get_lossless_quality(file_path)
    elif file_path.lower().endswith(('.mp3', '.aac', '.ogg', '.opus', '.mpc', '.atrac')):
        quality = get_lossy_quality(file_path)
    else:
        return None

    if quality:
        quality.update(metadata)
    return quality

def compare_quality(new_quality, existing_quality):
    if new_quality['format'] in ['wav', 'aiff', 'pcm', 'bwf']:
        return (new_quality['bit_depth'], new_quality['sample_rate'], new_quality['channels']) > \
               (existing_quality['bit_depth'], existing_quality['sample_rate'], existing_quality['channels'])
    elif new_quality['format'] in ['flac', 'alac', 'wma', 'ape', 'wv', 'tta', 'm4a', 'mp4']:
        return (new_quality['bit_depth'], new_quality['sample_rate'], new_quality['channels']) > \
               (existing_quality['bit_depth'], existing_quality['sample_rate'], existing_quality['channels'])
    elif new_quality['format'] in ['mp3', 'aac', 'ogg', 'opus', 'mpc', 'atrac']:
        return (new_quality['bitrate'], new_quality['sample_rate'], new_quality['channels']) > \
               (existing_quality['bitrate'], existing_quality['sample_rate'], existing_quality['channels'])
    else:
        return False

def organize_music_library(source_folder, destination_folder, review_folder, test_mode=False, copy_mode=False):
    library = {}
    log_entries = []

    for root, _, files in os.walk(source_folder):
        for file in files:
            if not file.lower().endswith(SUPPORTED_FORMATS):
                continue

            file_path = os.path.join(root, file)
            quality = get_audio_quality(file_path)
            if not quality:
                log_entries.append(f"Moving {file_path} to review folder due to insufficient metadata or corruption.")
                if not test_mode:
                    os.makedirs(review_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(review_folder, file))
                continue

            key = (quality['title'], quality['artist'], quality['album'])
            if key not in library:
                library[key] = file_path
                log_entries.append(f"Adding {file_path} to library.")
            else:
                existing_quality = get_audio_quality(library[key])
                if not existing_quality:
                    continue

                if compare_quality(quality, existing_quality):
                    log_entries.append(f"Replacing {library[key]} with {file_path} due to higher quality.")
                    if not test_mode and not copy_mode:
                        os.remove(library[key])
                    library[key] = file_path
                else:
                    log_entries.append(f"Skipping {file_path} due to lower quality.")
                    if not test_mode and not copy_mode:
                        os.remove(file_path)

    for (title, artist, album), file_path in library.items():
        artist_folder = os.path.join(destination_folder, artist)
        album_folder = os.path.join(artist_folder, album)
        os.makedirs(album_folder, exist_ok=True)
        log_entries.append(f"Copying {file_path} to {album_folder}.")
        if not test_mode:
            if copy_mode:
                shutil.copy(file_path, os.path.join(album_folder, os.path.basename(file_path)))
            else:
                shutil.move(file_path, os.path.join(album_folder, os.path.basename(file_path)))

    with open("organize_music_log.txt", "w") as log_file:
        log_file.write("\n".join(log_entries))


if __name__ == "__main__":
    source_folder = "path/to/your/source/folder"
    destination_folder = "path/to/your/destination/folder"
    review_folder = "path/to/your/review/folder"
    test_mode = False  # Set to True to test without moving files
    copy_mode = False  # Set to True to copy files instead of moving

    organize_music_library(source_folder, destination_folder, review_folder, test_mode, copy_mode)