# STT Demo - Speech-to-Text Demonstration

A flexible, configuration-based speech-to-text demonstration framework that supports multiple STT models and can run entirely on a local GPU with 8GB memory.

## Features

- **Multiple STT Models**: Easy switching between different models via configuration
- **Dual Input Support**: Both file-based and real-time microphone transcription
- **GPU Optimized**: Designed for 8GB GPU deployment with memory-efficient models
- **Modular Architecture**: Plugin-based design for easy model integration
- **Configuration-Based**: No code changes needed to switch models

## Currently Supported Models

- ✅ **Faster-Whisper** (OpenAI Whisper with CTranslate2) - Best for multilingual
- ✅ **NVIDIA Canary** (NeMo Framework) - Best for accuracy
- ✅ **Wav2Vec2** (HuggingFace Transformers) - Best for English real-time

## Requirements

- Python 3.8+
- NVIDIA GPU with 8GB VRAM (for GPU mode)
- CUDA 11.x or 12.x
- Linux, Windows, or macOS

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jprad/stt-demo.git
cd stt-demo
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install model-specific dependencies

**For Faster-Whisper (default):**
```bash
# CUDA dependencies
# For CUDA 12.x
pip install ctranslate2

# For CUDA 11.x
pip install ctranslate2==3.24.0
```

**For NVIDIA Canary:**
```bash
pip install nemo_toolkit[asr]
```

**For Wav2Vec2:**
```bash
pip install transformers torch torchaudio
```

### 5. Install PyAudio (for microphone support)

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Windows:**
```bash
pip install pyaudio
# If this fails, download wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```

## Configuration

Edit `config/config.yaml` to customize the demo:

```yaml
# Switch models by changing this value
active_model: faster_whisper

# Default input mode
default_input_mode: microphone

# Model-specific settings
models:
  faster_whisper:
    model_size: base  # Options: tiny, base, small, medium, large-v2, large-v3
    device: cuda      # Options: cuda, cpu, auto
    compute_type: int8  # Options: float16, int8, int8_float16
    language: en      # Leave empty for auto-detection
```

## Usage

### Real-time Microphone Transcription (Default)

```bash
python src/demo.py
```

or explicitly:

```bash
python src/demo.py --microphone
```

With time limit:

```bash
python src/demo.py --microphone --duration 60  # Record for 60 seconds
```

### File Transcription

```bash
python src/demo.py --file path/to/audio.wav
```

### List Audio Devices

```bash
python src/demo.py --list-devices
```

### Use Custom Configuration

```bash
python src/demo.py --config path/to/custom_config.yaml
```

## Model Switching

To switch between models, simply edit `config/config.yaml`:

```yaml
# Use Faster-Whisper (multilingual, balanced)
active_model: faster_whisper

# Or switch to NVIDIA Canary (best accuracy)
# active_model: nemo_canary

# Or switch to Wav2Vec2 (fast English)
# active_model: wav2vec2
```

No code changes required!

### Model Comparison

| Model | Memory | Speed | Accuracy | Languages | Best For |
|-------|--------|-------|----------|-----------|----------|
| **Faster-Whisper** | 1-5GB | Medium | Excellent | 99 | Multilingual, balanced |
| **Canary** | ~6GB | Fast | Best | Multilingual | Highest accuracy |
| **Wav2Vec2** | 2-4GB | Fastest | Good | English | Real-time English |

## Project Structure

```
stt-demo/
├── config/
│   └── config.yaml           # Configuration file
├── src/
│   ├── models/
│   │   ├── base_model.py     # Abstract base class for models
│   │   ├── faster_whisper_model.py  # Faster-Whisper implementation
│   │   ├── canary_model.py   # NVIDIA Canary implementation
│   │   └── wav2vec2_model.py # Wav2Vec2 implementation
│   ├── input_handlers/
│   │   ├── file_handler.py   # File input handler
│   │   └── microphone_handler.py  # Microphone input handler
│   └── demo.py               # Main application
├── requirements.txt
├── README.md
└── CLAUDE.md                 # AI assistant guide
```

## Adding New Models

To add a new STT model:

1. Create a new model class in `src/models/` that inherits from `BaseSTTModel`
2. Implement the required methods: `load_model()`, `transcribe_file()`, `transcribe_audio()`
3. Add model configuration to `config/config.yaml`
4. Update the model factory in `src/demo.py`

Example:

```python
from models.base_model import BaseSTTModel, TranscriptionResult

class MyNewModel(BaseSTTModel):
    def load_model(self):
        # Load your model here
        pass

    def transcribe_file(self, audio_path):
        # Implement file transcription
        pass

    def transcribe_audio(self, audio_data, sample_rate):
        # Implement real-time transcription
        pass
```

## Performance Tips

### For 8GB GPU:

**Faster-Whisper:**
- Use `model_size: base` or `small`
- Set `compute_type: int8` for reduced memory usage
- Enable VAD (Voice Activity Detection) to skip silence

**Canary:**
- Default `nvidia/canary-1b` fits well in 8GB
- Uses ~6GB VRAM

**Wav2Vec2:**
- Very memory efficient (2-4GB)
- Use `facebook/wav2vec2-base-960h` for even smaller footprint

### For Better Accuracy:

**Faster-Whisper:**
- Use `model_size: medium` or `large-v2` (if memory allows)
- Set `compute_type: float16`
- Increase `beam_size` (at the cost of speed)

**Canary:**
- Already state-of-the-art
- Enable punctuation: `pnc: yes`

**Wav2Vec2:**
- Use `facebook/wav2vec2-large-960h-lv60-self` (recommended)
- Best for clean English audio

### For Real-time Performance:

**Faster-Whisper:**
- Use smaller models (`tiny` or `base`)
- Reduce `chunk_duration` in config
- Disable VAD if experiencing delays

**Canary:**
- Fast by default
- Good balance of speed and accuracy

**Wav2Vec2:**
- Fastest option overall
- Ideal for real-time English transcription

## Troubleshooting

### CUDA Out of Memory

- Use smaller model size
- Switch to `int8` compute type
- Reduce batch size in config

### PyAudio Issues

- Make sure PortAudio is installed
- On Linux: `sudo apt-get install portaudio19-dev`
- Try reinstalling: `pip uninstall pyaudio && pip install pyaudio`

### No Audio Input Detected

- Run `python src/demo.py --list-devices` to see available devices
- Check system audio permissions
- Try a different microphone

## GPU Memory Requirements

| Model Size | FP16 | INT8 |
|------------|------|------|
| tiny       | ~1GB | ~1GB |
| base       | ~1GB | ~1GB |
| small      | ~2GB | ~1GB |
| medium     | ~5GB | ~3GB |
| large-v2   | ~10GB | ~5GB |

**Recommendation for 8GB GPU**: Use `base` or `small` with `int8` quantization.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
- [CTranslate2](https://github.com/OpenNMT/CTranslate2)

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check CLAUDE.md for development guidelines
