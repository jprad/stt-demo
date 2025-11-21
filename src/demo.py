"""
Main STT Demo Application
Provides a command-line interface for speech-to-text transcription
with support for both file and microphone input.
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Optional
import yaml

from models import FasterWhisperModel, CanaryModel, Wav2Vec2Model
from input_handlers import FileHandler, MicrophoneHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class STTDemo:
    """Main demo application class"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the STT demo.

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.model = None
        self.file_handler = FileHandler(
            self.config['audio']['supported_formats']
        )
        self.microphone_handler = None

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file: {e}")
            sys.exit(1)

    def _initialize_model(self) -> None:
        """Initialize the STT model based on configuration"""
        active_model = self.config['active_model']
        model_config = self.config['models'].get(active_model)

        if not model_config:
            logger.error(f"Configuration for model '{active_model}' not found")
            sys.exit(1)

        logger.info(f"Initializing model: {active_model}")

        # Model factory - add more models here as they're implemented
        if active_model == 'faster_whisper':
            self.model = FasterWhisperModel(model_config)
        elif active_model == 'nemo_canary':
            self.model = CanaryModel(model_config)
        elif active_model == 'wav2vec2':
            self.model = Wav2Vec2Model(model_config)
        else:
            logger.error(f"Unknown model: {active_model}")
            sys.exit(1)

        # Load the model
        self.model.load_model()
        logger.info("Model loaded successfully")

        # Print model info
        info = self.model.get_info()
        logger.info(f"Model info: {info}")

    def transcribe_file(self, file_path: str) -> None:
        """
        Transcribe audio from a file.

        Args:
            file_path: Path to the audio file
        """
        # Validate file
        if not self.file_handler.validate_file(file_path):
            return

        # Show file info
        file_info = self.file_handler.get_file_info(file_path)
        logger.info(f"File: {file_info['name']} ({file_info['size_mb']} MB)")

        # Initialize model if not already done
        if not self.model:
            self._initialize_model()

        # Transcribe
        print("\n" + "=" * 60)
        print("TRANSCRIBING...")
        print("=" * 60)

        start_time = time.time()
        result = self.model.transcribe_file(file_path)
        elapsed_time = time.time() - start_time

        # Display results
        self._display_result(result, elapsed_time)

        # Save to file if configured
        if self.config['output']['save_to_file']:
            self._save_transcription(result, file_info['name'])

    def transcribe_microphone(self, duration: Optional[int] = None) -> None:
        """
        Transcribe audio from microphone in real-time.

        Args:
            duration: Optional duration in seconds (None for continuous)
        """
        # Initialize model if not already done
        if not self.model:
            self._initialize_model()

        # Initialize microphone handler
        sample_rate = self.config['audio']['sample_rate']
        chunk_duration = self.config['audio']['chunk_duration']

        self.microphone_handler = MicrophoneHandler(
            sample_rate=sample_rate,
            chunk_duration=chunk_duration
        )

        print("\n" + "=" * 60)
        print("REAL-TIME TRANSCRIPTION")
        print("=" * 60)
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Chunk duration: {chunk_duration} seconds")
        if duration:
            print(f"Recording duration: {duration} seconds")
        else:
            print("Press Ctrl+C to stop recording")
        print("=" * 60)
        print("\nStarting recording in 3 seconds...")
        time.sleep(3)

        try:
            self.microphone_handler.start_recording()
            print("\n🎤 RECORDING... Speak now!\n")

            start_time = time.time()
            chunk_count = 0

            while True:
                # Check duration limit
                if duration and (time.time() - start_time) >= duration:
                    break

                # Get audio chunk
                audio_chunk = self.microphone_handler.get_audio_chunk(timeout=0.5)

                if audio_chunk is not None:
                    chunk_count += 1
                    print(f"[Chunk {chunk_count}] Processing...")

                    try:
                        # Transcribe chunk
                        result = self.model.transcribe_audio(
                            audio_chunk,
                            sample_rate
                        )

                        # Display result
                        if result.text.strip():
                            print(f"  → {result.text}")
                        else:
                            print("  → [No speech detected]")

                    except Exception as e:
                        logger.error(f"Transcription error: {e}")

        except KeyboardInterrupt:
            print("\n\nStopping recording...")
        finally:
            self.microphone_handler.stop_recording()
            total_time = time.time() - start_time
            print(f"\nRecording stopped. Total time: {total_time:.1f} seconds")

    def _display_result(self, result, elapsed_time: float) -> None:
        """Display transcription result"""
        print("\n" + "=" * 60)
        print("TRANSCRIPTION RESULT")
        print("=" * 60)
        print(f"\n{result.text}\n")

        if self.config['output']['show_timestamps'] and result.segments:
            print("-" * 60)
            print("SEGMENTS (with timestamps):")
            print("-" * 60)
            for i, segment in enumerate(result.segments, 1):
                start = segment['start']
                end = segment['end']
                text = segment['text']
                print(f"[{start:.2f}s - {end:.2f}s] {text}")

        print("-" * 60)
        print(f"Language: {result.language or 'Unknown'}")
        print(f"Processing time: {elapsed_time:.2f} seconds")
        print("=" * 60 + "\n")

    def _save_transcription(self, result, filename: str) -> None:
        """Save transcription to file"""
        output_dir = Path(self.config['output']['output_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create output filename
        base_name = Path(filename).stem
        output_file = output_dir / f"{base_name}_transcript.txt"

        # Write transcription
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.text)
            f.write("\n\n")
            f.write("-" * 60 + "\n")
            f.write(f"Language: {result.language}\n")

            if result.segments:
                f.write("\nSegments:\n")
                for segment in result.segments:
                    f.write(
                        f"[{segment['start']:.2f}s - {segment['end']:.2f}s] "
                        f"{segment['text']}\n"
                    )

        logger.info(f"Transcription saved to {output_file}")

    def list_devices(self) -> None:
        """List available audio input devices"""
        handler = MicrophoneHandler()
        devices = handler.get_device_list()

        print("\n" + "=" * 60)
        print("AVAILABLE AUDIO INPUT DEVICES")
        print("=" * 60)

        if not devices:
            print("No audio input devices found")
        else:
            for device in devices:
                print(f"\n[{device['index']}] {device['name']}")
                print(f"  Channels: {device['channels']}")
                print(f"  Sample Rate: {device['sample_rate']} Hz")

        print("=" * 60 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='STT Demo - Speech-to-Text Demonstration'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to configuration file'
    )

    parser.add_argument(
        '--file',
        type=str,
        help='Transcribe audio from file'
    )

    parser.add_argument(
        '--microphone',
        action='store_true',
        help='Transcribe from microphone (real-time)'
    )

    parser.add_argument(
        '--duration',
        type=int,
        help='Recording duration in seconds (for microphone mode)'
    )

    parser.add_argument(
        '--list-devices',
        action='store_true',
        help='List available audio input devices'
    )

    args = parser.parse_args()

    # Create demo instance
    demo = STTDemo(config_path=args.config)

    # Execute requested action
    if args.list_devices:
        demo.list_devices()

    elif args.file:
        demo.transcribe_file(args.file)

    elif args.microphone:
        demo.transcribe_microphone(duration=args.duration)

    else:
        # Default behavior based on config
        default_mode = demo.config.get('default_input_mode', 'microphone')

        if default_mode == 'microphone':
            print("Starting in microphone mode (default)")
            print("Use --file <path> to transcribe a file instead\n")
            demo.transcribe_microphone()
        else:
            parser.print_help()


if __name__ == '__main__':
    main()
