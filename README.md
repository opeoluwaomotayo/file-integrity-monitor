# File Integrity Monitor

A defensive Python cybersecurity project that records SHA-256 hashes of files in a selected directory and later reports files that were **added, modified, or deleted**.

## Why this project?

File-integrity monitoring helps demonstrate the security principle of detecting unexpected changes to important files. This project is designed for teaching, laboratory demonstrations, and a cybersecurity GitHub portfolio.

## Features

- Creates a SHA-256 baseline of regular files
- Detects added files
- Detects modified files
- Detects deleted files
- Shows the number of unchanged files
- Recursively scans subdirectories
- Ignores common development folders such as `.git`, `.venv`, and `__pycache__`
- Uses only the Python standard library
- Includes automated unit tests

## Project Structure

```text
file-integrity-monitor/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── main.py
├── integrity_monitor.py
├── examples/
│   └── demo.txt
└── tests/
    └── test_integrity_monitor.py
```

## Requirements

- Python 3.9 or later recommended
- No third-party packages

## Quick Start

Create a baseline for the included example directory:

```bash
python main.py init examples -b demo-baseline.json
```

Edit `examples/demo.txt`, and then check integrity:

```bash
python main.py check examples -b demo-baseline.json
```

Example result:

```text
MODIFIED (1):
  - demo.txt

UNCHANGED: 0
```

## Run the Tests

```bash
python -m unittest discover -s tests -v
```

## Ethical and Security Scope

This is a defensive monitoring tool. It reads files selected by the user to calculate cryptographic hashes; it does not modify monitored files, bypass access controls, or transmit file contents.

## Limitations

- A baseline stored beside monitored data can itself be altered; production tools should protect baselines appropriately.
- This educational version does not provide real-time monitoring.
- SHA-256 detects content changes but does not explain why a file changed.
- File permissions and metadata are not currently monitored.

## Future Improvements

- Real-time filesystem monitoring
- Signed or protected baselines
- File metadata checks
- CSV/JSON reports
- Desktop or web dashboard
- Email/notification integration for authorized environments

## Author

**Dr. Opeoluwa Omotayo Ajilore**  
Lecturer, Computer Science

## License

MIT License. See [LICENSE](LICENSE).
