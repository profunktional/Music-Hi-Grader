# Music Hi-Grader

## Overview

The Music Library Hi-Grader is a Python script designed to help you organize your music collection efficiently. It scans your music files, checks their integrity, extracts metadata, and organizes them into a structured library based on quality and metadata such as artist, album, or genre.

## Features

- **File Integrity Check**: Ensures that the music files are not corrupted.
- **Metadata Extraction**: Retrieves metadata such as title, artist, album, and genre.
- **Quality Assessment**: Determines the quality of audio files based on format-specific parameters.
- **Duplicate Handling**: Identifies and handles duplicate files, retaining the highest quality version.
- **Organized Library**: Moves or copies files to a structured library based on artist, album, or genre.
- **Logging**: Generates a detailed log of actions performed during the organization process.

## Supported Formats

The script supports a wide range of audio formats, including:
- WAV
- AIFF
- FLAC
- ALAC
- WMA
- APE
- WV
- TTA
- MP4
- M4A
- MP3
- AAC
- OGG
- OPUS
- MPC
- ATRAC

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/profunktional/music-hi-grader.git
   cd music-library-organizer
