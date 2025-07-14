# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Azure Computer Use Model sample repository that demonstrates how to use AI models capable of interacting with graphical user interfaces (GUIs) through natural language instructions. The Computer Use model can understand visual interfaces, take actions, and complete tasks by controlling a computer just like a human would.

## Common Commands

### Setup (Windows)
```powershell
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r computer-use\requirements.txt

# Set environment variables (PowerShell)
$env:AZURE_OPENAI_ENDPOINT = "your-endpoint"
$env:AZURE_OPENAI_API_KEY = "your-api-key"
```

### Running the application
```powershell
cd computer-use
python main.py --instructions "Your task here"

# With enhanced version (supports .env files)
python main_enhanced.py --instructions "Your task here"

# Interactive mode without autoplay
python main.py --autoplay false
```

### Testing
```powershell
# Basic test
python main.py --instructions "Open calculator"

# Browser test
python main.py --instructions "Open web browser and go to microsoft.com"
```

## Architecture

### Core Components

1. **cua.py** - Core Computer Use Agent implementation
   - `Agent` class: Manages the AI model interaction and state
   - `Scaler` class: Handles screen resolution scaling for consistent AI input

2. **local_computer.py** - Computer control implementation
   - `LocalComputer` class: Handles screenshot capture and mouse/keyboard control
   - Uses PyAutoGUI for cross-platform input simulation

3. **main.py** / **main_enhanced.py** - Entry points
   - Command-line argument parsing
   - Azure OpenAI / OpenAI client initialization
   - Main interaction loop

### Key Design Patterns

- **Async/Await**: Uses asyncio for non-blocking API calls
- **Safety Checks**: Requires user consent for potentially dangerous operations
- **Screen Scaling**: Normalizes screen resolution to 1024x768 for model consistency

## Environment Configuration

### Required Environment Variables
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_KEY`: Azure API key
- `OPENAI_API_KEY`: (Optional) OpenAI API key for non-Azure usage

### Using .env Files
The enhanced version supports loading from .env files:
1. Copy `.env.example` to `.env`
2. Add your credentials
3. Run `main_enhanced.py`

## Security Considerations

- Never commit API keys to the repository
- Use environment variables or .env files (which are gitignored)
- The model can control mouse and keyboard - use with caution
- Consider using `--autoplay false` for manual control over actions

## Development Guidelines

- Maintain Windows line endings (CRLF) for .bat files
- Test on Windows primarily (as per user requirement)
- Ensure all paths work with Windows backslashes
- Keep API keys secure and out of version control

## Common Issues

1. **Missing dependencies**: Run `pip install -r computer-use\requirements.txt`
2. **Permission errors**: May need to run as Administrator on Windows
3. **API key errors**: Check environment variables are set correctly
4. **Screen control issues**: Ensure no other automation tools are running