# Contributing Guide

[中文版](CONTRIBUTING.md) | **English**

Thank you for your interest in contributing to Code Health Monitor! We welcome contributions of all kinds.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [What Can I Contribute](#what-can-i-contribute)
- [Development Setup](#development-setup)
- [Commit Guidelines](#commit-guidelines)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## 🤝 Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all. By participating in this project, you agree to:

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 💡 What Can I Contribute

### 1. Report Bugs

Found a bug? Help us improve:
- Search [Issues](https://github.com/yzhucn/code-health/issues) to ensure it hasn't been reported
- If it's a new issue, create a new Issue
- Provide detailed reproduction steps
- Describe expected vs actual behavior
- Provide environment information (OS, Python version, etc.)

### 2. Suggest Features

Have a great idea? We'd love to hear it:
- Create a feature request in [Issues](https://github.com/yzhucn/code-health/issues)
- Clearly describe the feature's purpose and value
- Provide usage scenario examples if possible
- Discuss potential implementation approaches

### 3. Improve Documentation

Documentation can always be better:
- Fix spelling or grammar errors
- Improve clarity of existing documentation
- Add missing documentation
- Translate documentation to other languages

### 4. Submit Code

Contributing code is the most direct way to help:
- Fix bugs
- Implement new features
- Optimize performance
- Refactor code

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Git 2.0+
- Bash shell
- (Optional) DingTalk/Feishu account for testing notifications

### Clone Repository

```bash
# Fork the repository to your account
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/code-health.git
cd code-health

# Add upstream repository
git remote add upstream https://github.com/yzhucn/code-health.git
```

### Install Dependencies

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Copy configuration template
cp config.example.yaml config.yaml

# Edit configuration as needed
vim config.yaml
```

### Create Development Branch

```bash
# Create new branch from main
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Commit Guidelines

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation update
- `style`: Code formatting (no logic changes)
- `refactor`: Refactoring (neither new feature nor bug fix)
- `perf`: Performance optimization
- `test`: Testing related
- `chore`: Build process or auxiliary tools

#### Scope (Optional)

- `core`: Core functionality
- `report`: Report generation
- `dashboard`: Dashboard
- `notification`: Notification push
- `config`: Configuration
- `docs`: Documentation

#### Examples

```bash
# Good commit messages
feat(report): add monthly report generation
fix(notification): fix DingTalk push failure
docs(readme): update installation instructions

# Bad commit messages
update code
fix bug
update
```

### Detailed Commit Message Example

```
feat(dashboard): add code complexity trend chart

- Add complexity calculation module
- Integrate ECharts chart in dashboard
- Support 7/14/30 day time range selection

Closes #123
```

## 🎨 Code Style

### Python Code Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide:

```python
# Good example
def calculate_health_score(commit_data: dict) -> float:
    """
    Calculate code health score

    Args:
        commit_data: Commit data dictionary

    Returns:
        Health score (0-100)
    """
    if not commit_data:
        return 0.0

    score = 100.0
    # Calculation logic...
    return score

# Bad example
def calc(d):
    if not d: return 0
    s=100
    return s
```

**Code Style Points**:
- Use 4 spaces for indentation (no tabs)
- Use descriptive names for functions and classes
- Add docstrings
- Keep functions short (generally under 50 lines)
- Use type annotations (Python 3.8+)

### Shell Script Style

```bash
#!/bin/bash
# Brief description of script purpose

set -e  # Exit immediately on error

# Use meaningful variable names
REPORT_DATE=$(date +%Y-%m-%d)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function names use lowercase and underscores
generate_daily_report() {
    local date=$1
    echo "Generating daily report for $date..."
    # Implementation...
}

# Good example: Clear error handling
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found: $CONFIG_FILE" >&2
    exit 1
fi
```

## 🔄 Pull Request Process

### 1. Ensure Code is Up to Date

```bash
# Fetch upstream updates
git fetch upstream

# Merge into your branch
git checkout main
git merge upstream/main

# Update your feature branch
git checkout feature/your-feature-name
git rebase main
```

### 2. Test Your Changes

```bash
# Run existing tests (if any)
python3 -m pytest tests/

# Manually test core features
cd scripts
python3 daily-report.py
python3 weekly-report.py
```

### 3. Create Pull Request

- Push your branch to GitHub
- Create Pull Request on GitHub
- Fill in PR template (if available)
- Link related Issues (use `Closes #123`)

### 4. PR Description Template

```markdown
## 📝 Change Description

Briefly describe what this PR does.

## 🔧 Change Type

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance optimization
- [ ] Code refactoring

## ✅ Testing

Describe how you tested these changes:
- [ ] Manual testing passed
- [ ] Added unit tests
- [ ] Updated documentation

## 📸 Screenshots (if applicable)

If there are UI changes, provide screenshots.

## 📋 Checklist

- [ ] Code follows project style
- [ ] Commit messages follow conventions
- [ ] Added necessary documentation
- [ ] Tested all changes
- [ ] No sensitive information (Tokens, IPs, etc.)
```

### 5. Code Review

- Maintainers will review your code
- Changes may be requested
- Please respond to comments promptly
- Push updates after making changes

### 6. Merge

- After review approval, maintainers will merge your PR
- Your contribution will appear in the next release
- Thank you for your contribution! 🎉

## 🐛 Reporting Issues

When creating an Issue, please provide:

### Bug Report Template

```markdown
**Bug Description**
Brief description of the bug.

**Steps to Reproduce**
1. Execute '...'
2. Run '...'
3. See error '...'

**Expected Behavior**
Describe what you expected to happen.

**Actual Behavior**
Describe what actually happened.

**Environment**
- OS: [e.g. macOS 13.0, Ubuntu 22.04]
- Python Version: [e.g. 3.9.7]
- Git Version: [e.g. 2.39.0]
- Bash Version: [e.g. 5.1.16]

**Logs/Error Messages**
```
Paste relevant error messages or logs
```

**Screenshots**
If applicable, add screenshots to help explain the problem.

**Additional Information**
Any other information that might help solve the issue.
```

## 💭 Feature Requests

When creating a feature request, please provide:

### Feature Request Template

```markdown
**Feature Description**
Clear and concise description of the feature you want.

**Problem Context**
What problem does this feature solve? Why is it needed?

**Proposed Solution**
Describe how you'd like this feature to be implemented.

**Alternative Solutions**
Describe other solutions you've considered.

**Use Cases**
Provide 1-2 real-world usage scenario examples.

**Additional Information**
Any other relevant information or screenshots.
```

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/yzhucn/code-health/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yzhucn/code-health/discussions)
- **Email**: Contact maintainers through GitHub profile

## 🙏 Acknowledgments

Thanks to all contributors! Your efforts make this project better.

### Contributors List

<!-- Contributors list will be auto-generated here -->

View all contributors: [Contributors](https://github.com/yzhucn/code-health/graphs/contributors)

---

**Thank you again for your contribution!** 🎉

If you have any questions, feel free to ask in [Issues](https://github.com/yzhucn/code-health/issues).
