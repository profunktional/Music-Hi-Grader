import os
from mutagen import File

SUPPORTED_FORMATS = ('.wav', '.aiff', '.flac', '.alac', '.wma', '.ape', '.wv', '.tta', '.mp4', '.m4a', '.mp3', '.aac', '.ogg', '.opus', '.mpc', '.atrac')

def scan_audio_files(directory):
    format_count = {}
    log_entries = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(SUPPORTED_FORMATS):
                try:
                    audio = File(file_path)
                    if audio is not None:
                        file_format = file.split('.')[-1].lower()
                        format_count[file_format] = format_count.get(file_format, 0) + 1
                        log_entries.append(f"Found {file_format.upper()} file: {file_path}")
                    else:
                        log_entries.append(f"Unsupported or corrupted file: {file_path}")
                except Exception as e:
                    log_entries.append(f"Error processing {file_path}: {e}")

    return format_count, log_entries

def generate_report(directory, report_file="audio_formats_report.txt"):
    format_count, log_entries = scan_audio_files(directory)

    with open(report_file, "w") as report:
        report.write("Audio Formats Report\n")
        report.write("====================\n\n")
        for format, count in format_count.items():
            report.write(f"{format.upper()}: {count} files\n")
        report.write("\nDetailed Log:\n")
        report.write("=============\n")
        report.write("\n".join(log_entries))

if __name__ == "__main__":
    target_directory = "/Volumes/Media/"
    generate_report(target_directory)
