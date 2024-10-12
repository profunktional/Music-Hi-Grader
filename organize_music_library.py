import os
import shutil
import librosa
import audioread
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4
from mutagen.aiff import AIFF
from pydub import AudioSegment

SUPPORTED_FORMATS = ('.mp3', '.flac', '.ogg', '.wma', '.m4a', '.wav', '.aiff', '.alac', '.aac')
FORMAT_PRIORITY = {
    'flac': 1,
    'alac': 2,
    'wav': 3,
    'aiff': 4,
    'mp3': 5,
    'aac': 6,
    'ogg': 7,
    'wma': 8,
    'm4a': 9
}

def get_audio_metadata(file_path):
    try:
        if file_path.endswith('.mp3'):
            audio = MP3(file_path, ID3=EasyID3)
            bitrate = audio.info.bitrate
        elif file_path.endswith('.flac'):
            audio = FLAC(file_path)
            bitrate = audio.info.bitrate
        elif file_path.endswith('.ogg'):
            audio = OggVorbis(file_path)
            bitrate = audio.info.bitrate
        elif file_path.endswith('.m4a') or file_path.endswith('.alac') or file_path.endswith('.aac'):
            audio = MP4(file_path)
            bitrate = audio.info.bitrate
        elif file_path.endswith('.aiff'):
            audio = AIFF(file_path)
            bitrate = audio.info.bitrate
        else:
            audio = AudioSegment.from_file(file_path)
            bitrate = audio.frame_rate * audio.frame_width * 8
            return {'title': None, 'artist': None, 'album': None, 'bitrate': bitrate, 'metadata': {}}
        
        return {
            'title': audio.get('title', [None])[0],
            'artist': audio.get('artist', [None])[0],
            'album': audio.get('album', [None])[0],
            'format': file_path.split('.')[-1],
            'bitrate': bitrate,
            'metadata': dict(audio)
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {'title': None, 'artist': None, 'album': None, 'format': None, 'bitrate': None, 'metadata': {}}

def merge_metadata(existing_metadata, new_metadata):
    merged_metadata = existing_metadata.copy()
    for key, value in new_metadata.items():
        if key not in merged_metadata or not merged_metadata[key]:
            merged_metadata[key] = value
    return merged_metadata

def organize_music_library(source_folder, destination_folder, review_folder, test_mode=False, copy_mode=False):
    library = {}
    log_entries = []
    
    for root, _, files in os.walk(source_folder):
        for file in files:
            if not file.lower().endswith(SUPPORTED_FORMATS):
                continue
            
            file_path = os.path.join(root, file)
            metadata = get_audio_metadata(file_path)
            
            if metadata['title'] and metadata['artist'] and metadata['album']:
                key = (metadata['title'], metadata['artist'], metadata['album'])
                
                if key not in library:
                    library[key] = file_path
                    log_entries.append(f"Adding {file_path} to library.")
                else:
                    existing_format = library[key].split('.')[-1]
                    new_format = metadata['format']
                    
                    if FORMAT_PRIORITY[new_format] < FORMAT_PRIORITY[existing_format]:
                        log_entries.append(f"Replacing {library[key]} with {file_path} due to higher quality format.")
                        if not test_mode and not copy_mode:
                            os.remove(library[key])
                        library[key] = file_path
                    elif FORMAT_PRIORITY[new_format] == FORMAT_PRIORITY[existing_format]:
                        existing_bitrate = get_audio_metadata(library[key])['bitrate']
                        new_bitrate = metadata['bitrate']
                        
                        if new_bitrate > existing_bitrate:
                            log_entries.append(f"Replacing {library[key]} with {file_path} due to higher bitrate.")
                            if not test_mode and not copy_mode:
                                os.remove(library[key])
                            library[key] = file_path
                        elif new_bitrate == existing_bitrate:
                            existing_metadata = get_audio_metadata(library[key])['metadata']
                            new_metadata = metadata['metadata']
                            merged_metadata = merge_metadata(existing_metadata, new_metadata)
                            log_entries.append(f"Merging metadata for {file_path} with existing file.")
                            # Here you can save the merged metadata back to the file if needed
                        else:
                            log_entries.append(f"Skipping {file_path} due to lower bitrate.")
                            if not test_mode and not copy_mode:
                                os.remove(file_path)
                    else:
                        log_entries.append(f"Skipping {file_path} due to lower quality format.")
                        if not test_mode and not copy_mode:
                            os.remove(file_path)
            else:
                log_entries.append(f"Moving {file_path} to review folder due to insufficient metadata.")
                if not test_mode:
                    os.makedirs(review_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(review_folder, file))
    
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
    test_mode = True  # Set to False to actually move or copy files
    copy_mode = True  # Set to True to copy files instead of moving them
    
    organize_music_library(source_folder, destination_folder, review_folder, test_mode, copy_mode)
