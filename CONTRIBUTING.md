# Contributing to LastWarAutoBot Pro

Thank you for your interest in contributing! We welcome contributions from the community.

## Code of Conduct

Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue describing:
   - The feature and its benefits
   - Use cases
   - Implementation ideas (optional)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run tests: `pytest tests/`
6. Format code: `black src/` and `flake8 src/`
7. Commit changes: `git commit -m "Add amazing feature"`
8. Push to branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/LastWarAutoBot.git
cd LastWarAutoBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Coding Standards

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions/classes
- Add tests for new features
- Keep functions focused and small

### Commit Messages

- Use clear, descriptive messages
- Start with a verb (Add, Fix, Update, etc.)
- Reference issues if applicable

Example:
```
Add zombie hunting auto-heal feature (#123)

- Implement post-battle healing
- Add stamina threshold check
- Update tests
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to ask questions in GitHub Discussions or Issues.

Thank you for contributing! 🙏
