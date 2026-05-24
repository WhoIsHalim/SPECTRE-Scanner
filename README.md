# SPECTRE Scanner v3.0

![SPECTRE](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-purple)

**SPECTRE** is a High-Performance Asynchronous Reconnaissance Engine and Port Scanner. It leverages `asyncio` and `aiohttp` to perform lightning-fast mass scanning, banner grabbing, and HTTP title extraction with an extremely low memory footprint.

Developed by [Halim](https://github.com/WhoIsHalim).

## Features

- 🚀 **High Performance:** Completely asynchronous (Non-blocking I/O).
- 🧠 **Smart Memory Management:** Uses streaming IP architecture to prevent RAM exhaustion on massive subnets.
- 🎯 **Advanced Fingerprinting:** Regex-based signature matching engine to identify protocols, web servers, and specific services.
- 🕵️ **Banner Grabbing:** Protocol-aware banner extraction.
- 📊 **Rich Reporting:** Exports data automatically in `TXT`, `CSV`, `JSON`, and `SQLite`.
- 🛡️ **Custom Filters:** Target specific technologies or terms and ignore everything else.
- 💻 **Cross-Platform:** Beautiful Terminal UI that works flawlessly on both Windows and Linux.
- 🚦 **Rate Limiting:** Built-in connection throttlers (`asyncio.Semaphore`) to avoid socket exhaustion.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/WhoIsHalim/SPECTRE-Scanner.git
   cd SPECTRE-Scanner
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main file to launch the interactive Terminal UI:

```bash
python main.py
```

### Main Menu
- **[1] Start Scan**: Choose between a **Full Scan** (saves all open ports) or a **Custom Scan** (filters results based on `filter.txt`).
- **[2] Edit Config**: View paths for the configuration files (`config.yaml`, `ip_ranges.txt`, `ports.txt`, `fingerprints.json`, `filter.txt`).
- **[3] Show Statistics**: View the size and status of your generated reports.

### Configuration Files

On the first run, SPECTRE will automatically generate a `config/` directory with the following default files:

- `ip_ranges.txt`: Add your target IPs or CIDRs here (one per line).
- `ports.txt`: Specify ports to scan (e.g., `80,443,8080-8090`).
- `config.yaml`: Global settings for concurrency, timeouts, and active reporting modules.
- `fingerprints.json`: Define your custom regex signatures for deep service discovery.
- `filter.txt`: A list of substrings to match against when running a "Custom Scan".

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
