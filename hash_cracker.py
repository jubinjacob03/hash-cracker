#!/usr/bin/env python3

from api_handlers import gamma, alpha, beta, theta, delta, crackstation, hashes_org
import re
import os
import concurrent.futures
import argparse  

# Terminal badges for output
info = '\033[93m[!]\033[0m'
good = '\033[92m[+]\033[0m'
bad = '\033[91m[-]\033[0m'

# Hash functions lists 
md5 = [gamma, alpha, beta, theta, delta, crackstation, hashes_org]
sha1 = [alpha, beta, theta, delta, crackstation, hashes_org]
sha256 = [alpha, beta, theta, crackstation, hashes_org]
sha384 = [alpha, beta, theta, crackstation, hashes_org]
sha512 = [alpha, beta, theta, crackstation, hashes_org]

# Crack function to identify and use appropriate hash functions 
def crack(hashvalue):
    length_to_funcs = {
        32: ('MD5', md5),
        40: ('SHA1', sha1),
        64: ('SHA-256', sha256),
        96: ('SHA-384', sha384),
        128: ('SHA-512', sha512)
    }
    hash_length = len(hashvalue)
    if hash_length in length_to_funcs:
        print(f'{info} Hash function : {length_to_funcs[hash_length][0]}')
        for api in length_to_funcs[hash_length][1]:
            r = api(hashvalue, length_to_funcs[hash_length][0].lower())
            if r is not None:  
                return r
        print(f'{bad} Hash not found in any database.')
    else:
        print(f'{bad} This hash type is not supported.')
    return None

# Results dictionary 
result = {}

# Threaded cracking function 
def threaded(hashvalue):
    resp = crack(hashvalue)
    if resp:
        print(f'{good} Original word : {resp}')
        result[hashvalue] = resp
    else:
        print(f'{bad} Hash was not found.')

# Function to mine hashes from file
def miner(file_path, thread_count):
    lines = []
    found = set()
    with open(file_path, 'r') as f:
        lines = [line.strip('\n') for line in f]
    for line in lines:
        matches = re.findall(
            r'[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}', line)
        found.update(matches)
    print(f'{info} Hashes found: {len(found)}')
    threadpool = concurrent.futures.ThreadPoolExecutor(
        max_workers=thread_count)
    futures = [threadpool.submit(threaded, hashvalue) for hashvalue in found]
    for i, _ in enumerate(concurrent.futures.as_completed(futures)):
        if i + 1 == len(found) or (i + 1) % thread_count == 0:
            print(f'{info} Progress: {i + 1}/{len(found)}', end='\r')
    print("\n\n")

# Function for single hash cracking 
def single(hashvalue):
    result = crack(hashvalue)
    if result:
        print(f'{good} Original word : {result}')
    else:
        print(f'{bad} Hash was not found in any database.')

# Function to display the menu
def display_menu():
    print()
    print("╔═══════════════════════════════╗")
    print("║        Hash cracker v2        ║")
    print("╠═══════════════════════════════╣")
    print("║  1. Crack a single hash       ║")
    print("║  2. Crack hashes from a file  ║")
    print("║  3. Exit                      ║") 
    print("╚═══════════════════════════════╝")

# Main function
def main():
    parser = argparse.ArgumentParser(description='Hash cracker CLI tool')
    parser.add_argument('-c', '--crack', metavar='HASH', help='Crack a single hash')
    parser.add_argument('-f', '--file', metavar='FILE', help='Crack hashes from a file')

    args = parser.parse_args()

    if args.crack:
        single(args.crack)
    elif args.file:
        thread_count = input(f"{info} Enter the number of threads (default is 4): ")
        thread_count = int(thread_count) if thread_count.isdigit() else 4
        miner(args.file, thread_count)
    else:
        while True:
            display_menu()
            choice = input(f"{info} Enter your choice (1-3): ")

            if choice == '1':
                hashvalue = input(f"{info} Enter the hash to crack: ")
                single(hashvalue)
            elif choice == '2':
                file_path = input(f"{info} Enter the path to the input file: ")
                thread_count = input(f"{info} Enter the number of threads (default is 4): ")
                thread_count = int(thread_count) if thread_count.isdigit() else 4
                miner(file_path, thread_count)
            elif choice == '3':
                print(f"{info} Exiting...")
                break
            else:
                print(f"{bad} Invalid choice. Please enter a number between 1 and 3.")

if __name__ == '__main__':
    main()
