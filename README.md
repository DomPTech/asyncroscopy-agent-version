# Asyncroscopy:
- Enabling smart microscopy via asynchronous servers

---

# Q. Are you here to just directly dive in and do some hands on??
see: [Tutorial notebook](notebooks/1_Client_tutorial.ipynb)

---


## Project layout(Updated on 20th Feb 2026)

```
.
├── src/
│   ├── Microscope.py              # Main device — owns AutoScript connection and all acquisition commands
│   ├── detectors/
│   │   ├── HAADF.py               # HAADF detector settings device
│   │   ├── EELS.py                # EELS detector settings device (stub)
│   │   ├── EDS.py                 # EDS detector settings device (stub)
│   │   └── CEOS.py                # CEOS detector settings device (stub)
│   ├── hardware/
│   │   ├── STAGE.py               # Stage position and movement device
│   │   └── BEAM.py                # Beam blanking and current device
│   └── acquisition/
│       └── advanced_acquisition.py  # Multi-detector acquisition helpers (stub)
├── tests/
│   ├── conftest.py                # Shared pytest fixtures (DeviceTestContext proxies)
│   ├── test_microscope.py         # Microscope device tests
│   ├── test_acquisition.py        # Acquisition tests
│   └── detectors/
│       └── test_HAADF.py          # HAADF device tests
├── notebooks/
│   └── Client.ipynb               # Tutorial: connect → configure → acquire → display
├── llm-context/                   # AutoScript and PyTango API corpus for LLM-assisted development
├── AS_commands.txt                # AutoScript API reference snippets
└── pyproject.toml
```

### Contributing and Design principle
See - docs/dev_guide.md

## Requirements and Installation

See - pyproject.toml

```bash
uv sync .
```


## Running tests

```bash
uv run pytest tests/ -v
```



