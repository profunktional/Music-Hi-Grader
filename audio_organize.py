import os
import shutil
import re
import logging
from tinytag import TinyTag

SUPPORTED_FORMATS = ('.mp3', '.flac', '.ogg', '.wma', '.m4a', '.wav', '.aiff')

FORMAT_PRIORITY = {
    'flac': 1,
    'alac': 2,
    'wav': 3,
    'aiff': 4,
    'mp3': 5,
    'aac': 6,
    'ogg': 7
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_audio_info(file_path):
    try:
        tag = TinyTag.get(file_path)
        file_extension = os.path.splitext(file_path)[1][1:].lower()
        return {
            'title': tag.title if tag.title else 'Unknown Title',
            'artist': tag.artist if tag.artist else 'Unknown Artist',
            'album': tag.album if tag.album else 'Unknown Album',
            'length': tag.duration if tag.duration else 0,
            'bitrate': tag.bitrate if tag.bitrate else 0,
            'filesize': os.path.getsize(file_path),
            'bitdepth': tag.bitrate / tag.samplerate if tag.bitrate and tag.samplerate else 0,
            'samplerate': tag.samplerate if tag.samplerate else 0,
            'format_priority': FORMAT_PRIORITY.get(file_extension, 999),
            'path': file_path
        }
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return {
            'title': 'Unknown Title',
            'artist': 'Unknown Artist',
            'album': 'Unknown Album',
            'length': 0,
            'bitrate': 0,
            'filesize': 0,
            'bitdepth': 0,
            'samplerate': 0,
            'format_priority': 999,
            'path': file_path
        }

def is_better_quality(info1, info2):
    if info1['format_priority'] < info2['format_priority']:
        return True
    if info1['format_priority'] == info2['format_priority']:
        if info1['bitrate'] > info2['bitrate']:
            return True
        if info1['filesize'] > info2['filesize']:
            return True
        if info1['bitdepth'] > info2['bitdepth']:
            return True
        if info1['samplerate'] > info2['samplerate']:
            return True
        if info1['length'] > info2['length']:
            return True
    return False

def find_duplicates(music_folder):
    files_info = {}
    duplicates = []

    for root, _, files in os.walk(music_folder):
        for file in files:
            if file.endswith(SUPPORTED_FORMATS):
                file_path = os.path.join(root, file)
                info = get_audio_info(file_path)
                key = (info['title'], info['artist'])

                if key in files_info:
                    existing_file = files_info[key]
                    logging.info(f"Comparing:\n1. {existing_file['path']} (Format: {existing_file['format_priority']}, Bitrate: {existing_file['bitrate']} kbps, Filesize: {existing_file['filesize']} bytes, Bitdepth: {existing_file['bitdepth']}, Samplerate: {existing_file['samplerate']} Hz, Duration: {existing_file['length']} s)\n2. {file_path} (Format: {info['format_priority']}, Bitrate: {info['bitrate']} kbps, Filesize: {info['filesize']} bytes, Bitdepth: {info['bitdepth']}, Samplerate: {info['samplerate']} Hz, Duration: {info['length']} s)")
                    if is_better_quality(info, existing_file):
                        duplicates.append(existing_file['path'])
                        files_info[key] = info
                    else:
                        duplicates.append(file_path)
                else:
                    files_info[key] = info

    return duplicates

def remove_duplicates(duplicates):
    for file in duplicates:
        os.remove(file)

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name)

def organize_music(music_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(music_folder):
        for file in files:
            if file.endswith(SUPPORTED_FORMATS):
                file_path = os.path.join(root, file)
                info = get_audio_info(file_path)
                artist_folder = os.path.join(output_folder, sanitize_filename(info['artist']))
                album_folder = os.path.join(artist_folder, sanitize_filename(info['album']))

                if not os.path.exists(album_folder):
                    os.makedirs(album_folder)

                shutil.move(file_path, os.path.join(album_folder, file))

if __name__ == '__main__':
    music_folder = '/Volumes/T7 Media/MasterMusicLibrary/'
    output_folder = '/Volumes/T7 Media/MusicLibrary'

    duplicates = find_duplicates(music_folder)
    input("Press Enter to remove duplicates...")
    remove_duplicates(duplicates)
    organize_music(music_folder, output_folder)