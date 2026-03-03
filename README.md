Enabling smart microscopy via asynchronous servers

![Structure Diagram](structure_overview.png)

## Installation

### Standard Installation (Full)
To install with all dependencies including Autoscript support:
```bash
pip install "asyncroscopy[autoscript] @ git+https://github.com/DomPTech/asyncroscopy.git"
```

### Minimal Installation (Integrators)
To install only core dependencies (e.g., for agents that don't host the Autoscript server):
```bash
pip install "asyncroscopy @ git+https://github.com/DomPTech/asyncroscopy.git"
```

### Development with `uv`
If you are developing in this repo and have the Autoscript wheels in `AS_1.14_wheels/`:
```bash
uv sync --all-extras
```
Without the wheels, use:
```bash
uv sync
```
