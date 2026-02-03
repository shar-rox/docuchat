# Contributing to DocuChat

Thank you for your interest in contributing to DocuChat! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/shar-rox/docuchat.git
   cd docuchat
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and write tests

3. Run tests:
   ```bash
   pytest tests/ -v
   ```

4. Format code:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. Push to your fork and submit a pull request

## Commit Message Format

We follow conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `style:` - Formatting changes
- `chore:` - Maintenance tasks

## Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for all public functions/classes
- Keep functions focused and under 50 lines when possible

## Testing

- Write unit tests for new functionality
- Maintain test coverage above 80%
- Include integration tests for major features

## Pull Request Process

1. Update README.md with details of interface changes
2. Update documentation if needed
3. Ensure all tests pass
4. Request review from maintainers

## Questions?

Feel free to open an issue for any questions or concerns!
