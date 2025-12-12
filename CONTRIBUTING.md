# Contributing to Video Upscaler Pro

Thank you for your interest in contributing to Video Upscaler Pro! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include:

- **Clear title**: Describe the issue concisely
- **Steps to reproduce**: Detailed steps to reproduce the behavior
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, Python version, GPU model, etc.
- **Logs**: Any relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title**: Describe the enhancement
- **Use case**: Why is this enhancement useful?
- **Proposed solution**: How should it work?
- **Alternatives**: Any alternative solutions considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

## 🔧 Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/video-upscaler-pro.git
   cd video-upscaler-pro
   ```

2. Install dependencies:
   ```bash
   # Windows
   install.bat

   # Linux/macOS
   ./install.sh
   ```

3. Install development dependencies:
   ```bash
   pip install pytest black flake8 pre-commit
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use **Black** for code formatting
- Use **Flake8** for linting
- Maximum line length: 100 characters
- Use type hints where appropriate

### Code Formatting

Format your code before committing:

```bash
# Format with Black
black src/

# Check with Flake8
flake8 src/
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `SpatialUpscaler`)
- **Functions/Methods**: `snake_case` (e.g., `upscale_video`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_SCALE_FACTOR`)
- **Private methods**: `_leading_underscore` (e.g., `_load_model`)

### Documentation

- Use docstrings for all public classes and functions
- Follow Google style docstrings:

```python
def upscale_video(input_path: str, scale_factor: int) -> dict:
    """
    Upscale a video using AI model.

    Args:
        input_path: Path to input video
        scale_factor: Upscaling factor (2, 4, or 8)

    Returns:
        dict: Processing results with 'success', 'output_path', 'metrics'

    Raises:
        ValueError: If scale_factor is invalid
        FileNotFoundError: If input_path doesn't exist
    """
    pass
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_video_processor.py

# Run with coverage
pytest --cov=src --cov-report=html
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names

Example:

```python
def test_upscaler_with_valid_input():
    """Test upscaler with valid video input"""
    upscaler = SpatialUpscaler('realesrgan', scale_factor=2)
    result = upscaler.upscale_video('test_video.mp4', 'output.mp4')
    assert result['success'] == True
```

## 🏗️ Project Structure

```
video-upscaler-pro/
├── src/
│   ├── models/          # AI model wrappers
│   ├── processors/      # Video processing
│   ├── ui/              # User interface
│   └── utils/           # Utilities
├── tests/               # Test files
├── docs/                # Documentation
└── benchmarks/          # Performance tests
```

## 📚 Adding New Features

### Adding a New AI Model

1. Create model wrapper in `src/models/`
2. Implement the required interface
3. Add tests in `tests/`
4. Update documentation
5. Add model to UI dropdown

Example structure:

```python
# src/models/new_model.py
from typing import Dict, Optional, Callable

class NewModel:
    def __init__(self, device: str = 'cuda'):
        self.device = device
        self.model = self._load_model()

    def _load_model(self):
        """Load the model weights"""
        pass

    def upscale(self, image):
        """Upscale a single image"""
        pass
```

### Adding New Features to UI

1. Update `src/ui/gradio_app.py`
2. Add new UI components
3. Implement callback functions
4. Test in browser
5. Update screenshots in docs

## 🐛 Debugging

### Enable Debug Mode

Set environment variable:
```bash
export DEBUG=1  # Linux/macOS
set DEBUG=1     # Windows
```

### Common Issues

**Import errors**: Ensure virtual environment is activated
**CUDA errors**: Check CUDA installation and GPU compatibility
**Memory errors**: Reduce batch size or use smaller model

## 🔄 Git Workflow

1. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Commit your changes**:
   ```bash
   git commit -m "Add: Description of your changes"
   ```

   Commit message prefixes:
   - `Add:` New feature
   - `Fix:` Bug fix
   - `Update:` Changes to existing features
   - `Docs:` Documentation changes
   - `Test:` Test additions or changes
   - `Refactor:` Code refactoring

3. **Push to your fork**:
   ```bash
   git push origin feature/my-new-feature
   ```

4. **Create Pull Request** on GitHub

## 📋 Checklist for Pull Requests

- [ ] Code follows project style guidelines
- [ ] Code is formatted with Black
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with main branch

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

- 🧠 **AI Models**: Integration of new upscaling models
- ⚡ **Performance**: Optimization and speed improvements
- 🎨 **UI/UX**: Interface improvements and design
- 📖 **Documentation**: Guides, tutorials, translations
- 🧪 **Testing**: Unit tests, integration tests
- 🐛 **Bug Fixes**: Fixing reported issues

## 💬 Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Requests**: Code contributions

## 📜 Code of Conduct

Be respectful and inclusive. We're all here to learn and improve the project together.

## ❓ Questions?

If you have questions about contributing, feel free to:
- Open a GitHub Discussion
- Comment on relevant issues
- Reach out to maintainers

Thank you for contributing to Video Upscaler Pro! 🎉
