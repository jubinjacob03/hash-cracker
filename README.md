# Advanced Hash Cracker

An advanced hash cracking tool with support for multiple hashing algorithms, multithreading, and integration with online hash cracking APIs.

## Features
- Supports MD5, SHA-1, SHA-256, SHA-384, and SHA-512
- Multithreading for improved performance
- Integration with multiple online hash cracking APIs
- Brute-force attack using a wordlist

## Installation
1. Clone the repository
2. Install the required packages
```sh
pip install -r requirements.txt
```

## Usage

- python hash_cracker.py -s <hash>

```sh
python hash_cracker.py -s 5f4dcc3b5aa765d61d8327deb882cf99
```
```sh
python hash_cracker.py -f hashes.txt
```
```sh
python hash_cracker.py -d /path/to/directory
```
```sh
python hash_cracker.py -s 5f4dcc3b5aa765d61d8327deb882cf99 -w wordlist.txt
```
