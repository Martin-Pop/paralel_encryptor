# AES-GCM File Encryptor

> ⚠️ **WARNING: WORK IN PROGRESS**
>
> This project is currently in development.
> * There may be critical bugs leading to data corruption.
> * **Do not use this tool to encrypt important or sensitive data without having a backup.**

---

## Overview

This is a Python tool designed for encrypting and decrypting files
using **AES-256-GCM** (Galois/Counter Mode). Uses **multiprocessing** and **memory-mapped files (`mmap`)**.
This allows it to process data chunks in parallel.

---

## Key Features

* **Algorithm:** AES-256-GCM (Authenticated Encryption).
* **Parallel Processing:** Uses a worker pool to encrypt/decrypt chunks concurrently.
* **Memory Efficiency:** Utilizes `mmap` to handle files larger than available RAM.

---

## Requirements

* Python 3.8+
* `cryptography` library

```bash
pip install cryptography
```

---

## How It Works

The tool splits the input file into fixed-size chunks to allow parallel processing.
Encryption: * Reads N bytes of raw data.
Writes N + 16 bytes (Encrypted Data + 16-byte Auth Tag).
Decryption: * Reads N + 16 bytes.
Writes N bytes of raw data.
File Structure:
Header (12 bytes): 8 bytes for nonce and 4 bytes for chunk size.

---

## Known Issues & Limitations

- Parameters are not yet validated.
- Unexpected crashes might not terminate all processes.
- Keyboard interrupt while **starting processes** will result in frozen console!
- There is no limit for worker count, however high number can result with freeze.
---

## Usage

### 1. Installation

1. Clone the repository or download the zip and extract it.
2. Install required dependencies

### 2. Running the Script
The script is run via the command line. You must specify whether you want to encrypt (-e) or decrypt (-d) the file.
```Bash
python main.py [mode] -i <input_file> -o <output_file> -k <key> [options]
```

| Argument    | Flag              | Required | Description                                                   |
|-------------|-------------------|----------|---------------------------------------------------------------|
| Mode        | -e, --encrypt     | Yes*     | Encrypt the input file.                                      |
| Mode        | -d, --decrypt     | Yes*     | Decrypt the input file.                                      |
| Input       | -i, --input       | Yes      | Path to the source file.                                     |
| Output      | -o, --output      | Yes      | Path to the destination file.                                |
| Key         | -k, --key         | Yes      | The encryption key string. Ensure it is strong!              |
| Chunk Size  | -c, --chunk-size  | No       | Size of data chunks in bytes. Default: 1048576 (1MB).        |
| Workers     | -w, --workers     | No       | Number of parallel worker processes. Default: 2.             |

---

## Errors

Errors are printed to the console as well as logged into file 'app.log' found in the same directory as 'main.py'
. Log file also contains traceback.

---

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
