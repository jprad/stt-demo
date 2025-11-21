# CLAUDE.md - AI Assistant Guide for stt-demo

**Last Updated**: 2025-11-21
**Repository**: jprad/stt-demo
**Project Type**: Speech-to-Text Demo Application

---

## Project Overview

This repository contains a Speech-to-Text (STT) demonstration application designed for local GPU deployment with 8GB memory.

### Purpose
- Demonstrate speech-to-text capabilities with local GPU inference
- Provide a flexible, configuration-based framework for easy model switching
- Support both file-based and real-time microphone transcription
- Serve as a reference implementation for STT integration without requiring custom code changes

### Key Features
- **Model Agnostic**: Switch between different STT models via configuration file
- **Dual Input Support**: Both audio file transcription and real-time microphone input
- **GPU Optimized**: Memory-efficient implementation for 8GB GPU deployment
- **Plugin Architecture**: Easy integration of new models through abstract base class

---

## Repository Structure

```
stt-demo/
├── config/
│   └── config.yaml                    # Main configuration file for model switching
├── src/
│   ├── __init__.py
│   ├── demo.py                        # Main demo application
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py              # Abstract base class for STT models
│   │   └── faster_whisper_model.py    # Faster-Whisper implementation
│   └── input_handlers/
│       ├── __init__.py
│       ├── file_handler.py            # Audio file input handler
│       └── microphone_handler.py      # Real-time microphone handler
├── requirements.txt                   # Python dependencies
├── README.md                          # User-facing documentation
├── CLAUDE.md                          # This file - AI assistant guide
└── .gitignore                         # Git ignore rules
```

---

## Development Workflow

### Branching Strategy

**Current Development Branch**: `claude/claude-md-mi86ooj52xk1yo4d-014xypTGDKhP4FXE5R7djLSA`

#### Branch Naming Conventions
- `main` - Production-ready code
- `develop` - Integration branch for features
- `claude/*` - AI assistant development branches (auto-generated with session IDs)
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates

#### Git Operations Best Practices

**Pushing Changes**:
```bash
git push -u origin <branch-name>
```
- CRITICAL: Branch names must start with `claude/` and end with matching session ID for AI assistant work
- Retry on network failures: up to 4 times with exponential backoff (2s, 4s, 8s, 16s)
- 403 errors indicate incorrect branch naming

**Fetching Updates**:
```bash
git fetch origin <branch-name>
git pull origin <branch-name>
```
- Prefer fetching specific branches over fetching all
- Apply same retry logic for network failures

### Commit Message Format

Follow conventional commit style:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(stt): add real-time transcription support

Implement WebSocket-based real-time speech recognition
with support for multiple audio formats.

Closes #123
```

---

## Code Conventions

### General Principles

1. **Clarity over Cleverness**: Write code that is easy to understand
2. **Modularity**: Keep functions and components small and focused
3. **Error Handling**: Always handle errors gracefully
4. **Documentation**: Document complex logic and public APIs
5. **Security**: Never commit sensitive data (API keys, credentials)

### File Naming
- Use snake_case for Python modules: `base_model.py`, `file_handler.py`
- Use PascalCase for class names: `BaseSTTModel`, `FasterWhisperModel`, `MicrophoneHandler`
- Use lowercase for config files: `config.yaml`, `.env.example`

### Code Style

**Python** (Primary Language):
- Follow PEP 8 style guide
- 4-space indentation
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for all classes and public methods
- Import order: standard library, third-party, local modules

### API Keys and Secrets
- NEVER commit API keys, tokens, or credentials
- Use environment variables for sensitive data
- Provide `.env.example` template files
- Add sensitive files to `.gitignore`

---

## Testing Guidelines

### Test Structure
```
tests/
├── unit/              # Unit tests for individual functions
├── integration/       # Integration tests for services
└── e2e/              # End-to-end tests
```

### Testing Principles
1. Write tests for new features before committing
2. Maintain test coverage above 80%
3. Use descriptive test names
4. Mock external dependencies (API calls, file I/O)
5. Test edge cases and error conditions

### Running Tests
```bash
# Run all tests
npm test          # Node.js
pytest            # Python

# Run specific test file
npm test -- path/to/test
pytest path/to/test.py

# Run with coverage
npm test -- --coverage
pytest --cov
```

---

## AI Assistant Guidelines

### Task Approach

1. **Understand First**: Read relevant code before making changes
2. **Plan**: Use TodoWrite tool for multi-step tasks
3. **Implement**: Make focused, incremental changes
4. **Test**: Verify changes work as expected
5. **Document**: Update relevant documentation
6. **Commit**: Create clear, descriptive commits

### Tool Usage Priority

**File Operations**:
- Use `Read` tool instead of `cat`
- Use `Edit` tool instead of `sed/awk`
- Use `Write` tool for new files (only when necessary)
- Prefer editing existing files over creating new ones

**Code Exploration**:
- Use `Task` tool with `subagent_type=Explore` for broad codebase analysis
- Use `Grep` tool for specific code searches
- Use `Glob` tool for finding files by pattern

**Avoid**:
- Don't create unnecessary documentation files
- Don't use emojis unless requested
- Don't commit without explicit user request
- Don't guess at API endpoints or URLs

### Security Considerations

When working with STT applications:
1. Validate audio input to prevent injection attacks
2. Sanitize transcription output before display
3. Rate limit API calls to prevent abuse
4. Secure WebSocket connections (use WSS)
5. Implement proper authentication for API endpoints
6. Handle PII (Personally Identifiable Information) appropriately
7. Follow GDPR/privacy guidelines for voice data

### Common STT Patterns

**Audio Processing**:
- Support common formats: WAV, MP3, FLAC, OGG
- Implement proper audio chunking for streaming
- Handle sample rate conversion
- Normalize audio levels

**Real-time Transcription**:
- Use WebSocket for bidirectional communication
- Implement reconnection logic
- Buffer audio during network issues
- Show interim results to users

**Error Handling**:
- Handle unsupported audio formats gracefully
- Provide fallbacks for failed transcriptions
- Implement timeout handling for long-running operations
- Log errors for debugging without exposing sensitive data

---

## Dependencies Management

### Package Installation
```bash
# Node.js
npm install <package>
npm install --save-dev <package>  # Dev dependencies

# Python
pip install <package>
pip install -r requirements.txt
```

### Version Pinning
- Pin major versions for stability
- Document breaking changes in commit messages
- Test after dependency updates

---

## Performance Considerations

### Audio Processing
- Process audio in chunks to avoid memory issues
- Use worker threads/processes for CPU-intensive tasks
- Implement caching for repeated operations
- Optimize model loading (load once, reuse)

### API Usage
- Implement request batching where possible
- Use connection pooling for HTTP clients
- Cache frequently requested data
- Implement exponential backoff for retries

---

## Debugging

### Common Issues

**Audio Not Processing**:
1. Check audio format compatibility
2. Verify sample rate matches expected input
3. Check for proper permissions (microphone access)
4. Validate audio data is not corrupt

**Transcription Errors**:
1. Check API key validity
2. Verify network connectivity
3. Check rate limits
4. Validate audio quality

### Logging
- Use structured logging (JSON format recommended)
- Include request IDs for tracing
- Log at appropriate levels (DEBUG, INFO, WARN, ERROR)
- Never log sensitive data (API keys, user content)

---

## Project-Specific Notes

### Current Status
- ✅ Core framework implemented with plugin architecture
- ✅ Faster-Whisper integration complete
- ✅ File and microphone input handlers implemented
- ✅ Configuration-based model switching system
- 🔄 Ready for additional model integrations
- Development branch: `claude/claude-md-mi86ooj52xk1yo4d-014xypTGDKhP4FXE5R7djLSA`

### Technology Stack
- **Language**: Python 3.8+
- **STT Engine**: Faster-Whisper (CTranslate2-based)
- **Audio Processing**: NumPy, PyAudio
- **Configuration**: PyYAML
- **GPU Support**: CUDA 11.x/12.x
- **Target Hardware**: 8GB GPU (NVIDIA)

### Architecture Patterns

#### Plugin-Based Model System
All STT models inherit from `BaseSTTModel` abstract class, which defines:
- `load_model()`: Load model into memory
- `transcribe_file(audio_path)`: Transcribe from file
- `transcribe_audio(audio_data, sample_rate)`: Transcribe from raw audio

This ensures consistency across models and allows switching via config without code changes.

#### Configuration-Driven Design
The `config/config.yaml` file controls:
- Active model selection
- Model-specific parameters (size, device, compute type)
- Audio settings (sample rate, chunk duration)
- Output preferences (timestamps, saving, etc.)

#### Input Handler Abstraction
Separate handlers for different input sources:
- `FileHandler`: Validates and processes audio files
- `MicrophoneHandler`: Captures real-time audio with PyAudio

### Adding New Models

To add a new STT model (e.g., NVIDIA Canary, Wav2Vec2):

1. **Create model class** in `src/models/`:
```python
from models.base_model import BaseSTTModel, TranscriptionResult

class YourNewModel(BaseSTTModel):
    def load_model(self):
        # Implementation
        pass

    def transcribe_file(self, audio_path):
        # Implementation
        pass

    def transcribe_audio(self, audio_data, sample_rate):
        # Implementation
        pass
```

2. **Add configuration** in `config/config.yaml`:
```yaml
models:
  your_new_model:
    model_name: path/to/model
    device: cuda
    # ... other params
```

3. **Register in demo.py** (line ~55 in `_initialize_model()`):
```python
elif active_model == 'your_new_model':
    from models.your_new_model import YourNewModel
    self.model = YourNewModel(model_config)
```

### Performance Optimization Tips

**For 8GB GPU Constraint:**
- Use quantized models (int8 compute type)
- Prefer smaller model sizes (base, small)
- Enable VAD to skip silence processing
- Monitor GPU memory with `nvidia-smi`

**For Real-time Transcription:**
- Reduce chunk duration (1-2 seconds)
- Use smaller models (tiny, base)
- Consider disabling VAD for lower latency

**For Accuracy:**
- Use larger models if memory allows (medium)
- Increase beam size in config
- Use float16 compute type instead of int8

---

## Resources

### STT Libraries & APIs
- **Faster-Whisper**: [GitHub](https://github.com/SYSTRAN/faster-whisper) - CTranslate2-based Whisper
- **OpenAI Whisper**: [GitHub](https://github.com/openai/whisper) - Original Whisper implementation
- **NVIDIA NeMo**: [Docs](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/) - ASR toolkit
- **Wav2Vec2**: [HuggingFace](https://huggingface.co/facebook/wav2vec2-base-960h) - Meta's STT model
- **CTranslate2**: [Docs](https://opennmt.net/CTranslate2/) - Fast inference engine

### Documentation
- [Faster-Whisper README](https://github.com/SYSTRAN/faster-whisper/blob/master/README.md)
- [PyAudio Documentation](https://people.csail.mit.edu/hubert/pyaudio/docs/)
- [NumPy Audio Processing](https://numpy.org/doc/stable/reference/routines.fft.html)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)

---

## Implementation Details

### Answered Design Decisions

1. **Target Platform**: Command-line application (Python)
2. **Audio Source**: Both microphone and file input supported
3. **Real-time vs Batch**: Both supported through dual input handlers
4. **Language Support**: Multilingual (Whisper supports 99 languages)
5. **Privacy**: On-device processing (local GPU, no cloud)
6. **Offline Support**: Fully offline after model download

### Key Classes

**BaseSTTModel** (`src/models/base_model.py`):
- Abstract base class for all STT models
- Defines `TranscriptionResult` dataclass for consistent output
- Methods: `load_model()`, `transcribe_file()`, `transcribe_audio()`, `get_info()`

**FasterWhisperModel** (`src/models/faster_whisper_model.py`):
- Implements Faster-Whisper with CTranslate2
- Configurable model size, device, compute type
- Supports VAD filtering and beam search

**FileHandler** (`src/input_handlers/file_handler.py`):
- Validates audio file formats
- Provides file information utilities
- Lists audio files in directories

**MicrophoneHandler** (`src/input_handlers/microphone_handler.py`):
- Real-time audio capture with PyAudio
- Queue-based audio chunk processing
- Context manager support for clean resource management

**STTDemo** (`src/demo.py`):
- Main application orchestrator
- Loads configuration and initializes models
- Provides CLI interface for all operations

---

## Contact & Support

For questions or issues:
- Create GitHub issues in the repository
- Follow conventional commit format
- Provide clear reproduction steps for bugs

---

**Note for AI Assistants**: This document should be updated as the project evolves. When significant architectural decisions are made or new patterns are established, update this file to reflect the current state of the codebase.
