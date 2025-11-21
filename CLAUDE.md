# CLAUDE.md - AI Assistant Guide for stt-demo

**Last Updated**: 2025-11-21
**Repository**: jprad/stt-demo
**Project Type**: Speech-to-Text Demo Application

---

## Project Overview

This repository contains a Speech-to-Text (STT) demonstration application. The project is currently in its initial setup phase.

### Purpose
- Demonstrate speech-to-text capabilities
- Provide reference implementation for STT integration
- Serve as a testing ground for voice recognition features

---

## Repository Structure

The repository is currently being initialized. Expected structure:

```
stt-demo/
├── src/                    # Source code
│   ├── components/        # UI components (if web-based)
│   ├── services/          # Core STT services
│   ├── utils/             # Utility functions
│   └── config/            # Configuration files
├── tests/                 # Test files
├── docs/                  # Additional documentation
├── examples/              # Usage examples
├── package.json           # Node.js dependencies (if applicable)
├── requirements.txt       # Python dependencies (if applicable)
├── README.md              # User-facing documentation
├── CLAUDE.md              # This file
└── .gitignore            # Git ignore rules
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
- Use kebab-case for files: `speech-recognition.js`, `audio-processor.py`
- Use PascalCase for component files: `TranscriptionDisplay.jsx`
- Use lowercase for config files: `config.json`, `.env.example`

### Code Style

**JavaScript/TypeScript**:
- Use ES6+ features
- Prefer `const` over `let`, avoid `var`
- Use arrow functions for callbacks
- 2-space indentation
- Semicolons required

**Python**:
- Follow PEP 8 style guide
- 4-space indentation
- Use type hints where appropriate
- Maximum line length: 100 characters

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
- Repository is in initial setup phase
- No code has been committed yet
- Development branch: `claude/claude-md-mi86ooj52xk1yo4d-014xypTGDKhP4FXE5R7djLSA`

### Next Steps
1. Initialize project structure
2. Set up development environment
3. Choose STT provider/library
4. Implement basic transcription functionality
5. Add tests and documentation

### Technology Stack (To Be Determined)
- **Frontend**: React, Vue, or vanilla JS
- **Backend**: Node.js, Python, or other
- **STT Engine**: Web Speech API, Whisper, Google Cloud Speech, AWS Transcribe, or other
- **Build Tools**: Webpack, Vite, or other

---

## Resources

### STT Libraries & APIs
- **Web Speech API**: Browser-native speech recognition
- **OpenAI Whisper**: Open-source, multilingual STT
- **Google Cloud Speech-to-Text**: Enterprise-grade API
- **AWS Transcribe**: Amazon's STT service
- **Mozilla DeepSpeech**: Open-source STT engine
- **AssemblyAI**: Modern STT API

### Documentation
- [Web Speech API Spec](https://wicg.github.io/speech-api/)
- [Audio Processing Basics](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [WebSocket Protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

---

## Questions for Consideration

Before implementing features, consider:

1. **Target Platform**: Web, desktop, mobile, or server-side?
2. **Audio Source**: Microphone, file upload, or both?
3. **Real-time vs Batch**: Streaming transcription or file processing?
4. **Language Support**: Single language or multilingual?
5. **Privacy**: On-device processing or cloud-based?
6. **Offline Support**: Required or network-only?

---

## Contact & Support

For questions or issues:
- Create GitHub issues in the repository
- Follow conventional commit format
- Provide clear reproduction steps for bugs

---

**Note for AI Assistants**: This document should be updated as the project evolves. When significant architectural decisions are made or new patterns are established, update this file to reflect the current state of the codebase.
