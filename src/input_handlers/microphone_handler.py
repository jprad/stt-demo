"""
Real-time microphone input handler.
Captures audio from the system microphone for live transcription.
"""

import logging
import numpy as np
import threading
import queue
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class MicrophoneHandler:
    """
    Handles real-time microphone input for live transcription.
    Captures audio in chunks and provides it for streaming transcription.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        chunk_duration: float = 2.0,
        callback: Optional[Callable] = None
    ):
        """
        Initialize the microphone handler.

        Args:
            sample_rate: Audio sample rate in Hz
            chunk_duration: Duration of each audio chunk in seconds
            callback: Optional callback function to process audio chunks
        """
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_size = int(sample_rate * chunk_duration)
        self.callback = callback

        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.stream = None
        self.audio_interface = None
        self.recording_thread = None

    def start_recording(self) -> None:
        """Start recording from the microphone"""
        if self.is_recording:
            logger.warning("Recording is already in progress")
            return

        try:
            import pyaudio

            self.audio_interface = pyaudio.PyAudio()

            # Open audio stream
            self.stream = self.audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )

            self.is_recording = True
            self.stream.start_stream()
            logger.info(f"Recording started (sample rate: {self.sample_rate} Hz)")

        except ImportError:
            raise ImportError(
                "PyAudio is not installed. "
                "Install it with: pip install pyaudio"
            )
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            raise

    def stop_recording(self) -> None:
        """Stop recording from the microphone"""
        if not self.is_recording:
            logger.warning("No recording in progress")
            return

        self.is_recording = False

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if self.audio_interface:
            self.audio_interface.terminate()
            self.audio_interface = None

        logger.info("Recording stopped")

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """
        Callback function called by PyAudio for each audio chunk.

        Args:
            in_data: Raw audio data
            frame_count: Number of frames
            time_info: Time information
            status: Status flags

        Returns:
            Tuple of (None, continue flag)
        """
        import pyaudio

        if status:
            logger.warning(f"Audio callback status: {status}")

        # Convert bytes to numpy array
        audio_data = np.frombuffer(in_data, dtype=np.int16)

        # Put audio data in queue
        self.audio_queue.put(audio_data)

        # Call user callback if provided
        if self.callback:
            try:
                self.callback(audio_data)
            except Exception as e:
                logger.error(f"Error in user callback: {e}")

        return (None, pyaudio.paContinue)

    def get_audio_chunk(self, timeout: float = 1.0) -> Optional[np.ndarray]:
        """
        Get the next audio chunk from the queue.

        Args:
            timeout: Maximum time to wait for audio chunk

        Returns:
            Audio data as numpy array, or None if timeout
        """
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def clear_queue(self) -> None:
        """Clear all pending audio chunks from the queue"""
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break

    def get_device_list(self) -> list:
        """
        Get list of available audio input devices.

        Returns:
            List of device information dictionaries
        """
        try:
            import pyaudio

            audio = pyaudio.PyAudio()
            devices = []

            for i in range(audio.get_device_count()):
                device_info = audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels'],
                        'sample_rate': int(device_info['defaultSampleRate'])
                    })

            audio.terminate()
            return devices

        except ImportError:
            logger.error("PyAudio not installed")
            return []
        except Exception as e:
            logger.error(f"Error getting device list: {e}")
            return []

    def __enter__(self):
        """Context manager entry"""
        self.start_recording()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_recording()
