"""
File-based audio input handler.
Supports various audio formats for batch transcription.
"""

import logging
import os
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class FileHandler:
    """
    Handles audio file input for transcription.
    Supports multiple audio formats.
    """

    def __init__(self, supported_formats: List[str] = None):
        """
        Initialize the file handler.

        Args:
            supported_formats: List of supported audio file extensions
        """
        self.supported_formats = supported_formats or [
            'wav', 'mp3', 'flac', 'ogg', 'm4a', 'aac', 'wma'
        ]
        # Normalize formats (remove dots, lowercase)
        self.supported_formats = [
            fmt.lower().lstrip('.') for fmt in self.supported_formats
        ]

    def is_supported(self, file_path: str) -> bool:
        """
        Check if a file format is supported.

        Args:
            file_path: Path to the audio file

        Returns:
            True if supported, False otherwise
        """
        ext = Path(file_path).suffix.lower().lstrip('.')
        return ext in self.supported_formats

    def validate_file(self, file_path: str) -> bool:
        """
        Validate that a file exists and is supported.

        Args:
            file_path: Path to the audio file

        Returns:
            True if valid, False otherwise
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False

        if not os.path.isfile(file_path):
            logger.error(f"Path is not a file: {file_path}")
            return False

        if not self.is_supported(file_path):
            ext = Path(file_path).suffix
            logger.error(
                f"Unsupported file format: {ext}. "
                f"Supported formats: {', '.join(self.supported_formats)}"
            )
            return False

        return True

    def get_file_info(self, file_path: str) -> dict:
        """
        Get information about an audio file.

        Args:
            file_path: Path to the audio file

        Returns:
            Dictionary with file information
        """
        path = Path(file_path)
        return {
            'path': str(path.absolute()),
            'name': path.name,
            'extension': path.suffix.lstrip('.'),
            'size_bytes': path.stat().st_size,
            'size_mb': round(path.stat().st_size / (1024 * 1024), 2)
        }

    def list_audio_files(self, directory: str) -> List[str]:
        """
        List all supported audio files in a directory.

        Args:
            directory: Path to the directory

        Returns:
            List of audio file paths
        """
        if not os.path.isdir(directory):
            logger.error(f"Directory not found: {directory}")
            return []

        audio_files = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path) and self.is_supported(file_path):
                audio_files.append(file_path)

        return sorted(audio_files)
