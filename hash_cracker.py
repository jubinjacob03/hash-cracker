#!/usr/bin/env python3

import re
import os
import argparse
import concurrent.futures
from api_handlers import alpha, beta, gamma, delta, theta

# Argument parser setup
parser = argparse.ArgumentParser(description='Advanced Hash Cracker')
parser.add_argument('-s', help='hash', dest='hash')
parser.add_argument('-f', help='file containing hashes', dest='file')
parser.add_argument('-d', help='directory containing hashes', dest='dir')
parser.add_argument('-w', help='wordlist file', dest='wordlist')
parser.add_argument('-t', help='number of threads', dest='threads', type=int, default=4)
args = parser.parse_args()

# Terminal colors for output
end = '\033[0m'
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
info = '\033[93m[!]\033[0m'
good = '\033[92m[+]\033[0m'
bad = '\033[91m[-]\033[0m'

cwd = os.getcwd()
directory = os.path.abspath(args.dir) if args.dir else None
file = args.file
wordlist = args.wordlist
thread_count = args.threads

if directory and directory[-1] == '/':
    directory = directory[:-1]

# Hash functions lists
md5 = [gamma, alpha, beta, theta, delta]
sha1 = [alpha, beta, theta, delta]
sha256 = [alpha, beta, theta]
sha384 = [alpha, beta, theta]
sha512 = [alpha, beta, theta]

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
            if r:
                return r
    else:
        print(f'{bad} This hash type is not supported.')
        return False

# Results dictionary
result = {}

# Threaded cracking function
def threaded(hashvalue):
    resp = crack(hashvalue)
    if resp:
        print(f'{hashvalue} : {resp}')
        result[hashvalue] = resp

# Function to search for hashes in directory
def grepper(directory):
    os.system(rf'''grep -Pr "[a-f0-9]{{128}}|[a-f0-9]{{96}}|[a-f0-9]{{64}}|[a-f0-9]{{40}}|[a-f0-9]{{32}}" {directory} --exclude=\*.{{png,jpg,jpeg,mp3,mp4,zip,gz}} |
        grep -Po "[a-f0-9]{{128}}|[a-f0-9]{{96}}|[a-f0-9]{{64}}|[a-f0-9]{{40}}|[a-f0-9]{{32}}" >> {cwd}/{directory.split('/')[-1]}.txt''')
    print(f'{info} Results saved in {directory.split("/")[-1]}.txt')

# Function to mine hashes from file
def miner(file):
    lines = []
    found = set()
    with open(file, 'r') as f:
        lines = [line.strip('\n') for line in f]
    for line in lines:
        matches = re.findall(r'[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}', line)
        found.update(matches)
    print(f'{info} Hashes found: {len(found)}')
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
    futures = [threadpool.submit(threaded, hashvalue) for hashvalue in found]
    for i, _ in enumerate(concurrent.futures.as_completed(futures)):
        if i + 1 == len(found) or (i + 1) % thread_count == 0:
            print(f'{info} Progress: {i + 1}/{len(found)}', end='\r')

# Function for single hash cracking
def single(args):
    result = crack(args.hash)
    if result:
        print(result)
    else:
        print(f'{bad} Hash was not found in any database.')

# Brute-force function using a wordlist
def brute_force(hashvalue, hash_funcs, wordlist):
    with open(wordlist, 'r') as wl:
        for word in wl:
            word = word.strip()
            for hash_func in hash_funcs:
                if hash_func(word.encode()).hexdigest() == hashvalue:
                    return word
    return False

# Main script execution
if directory:
    try:
        grepper(directory)
    except KeyboardInterrupt:
        pass
elif file:
    try:
        miner(file)
    except KeyboardInterrupt:
        pass
    with open(f'cracked-{file.split("/")[-1]}', 'w+') as f:
        for hashvalue, cracked in result.items():
            f.write(f'{hashvalue}:{cracked}\n')
    print(f'{info} Results saved in cracked-{file.split("/")[-1]}')
elif args.hash:
    single(args)
elif args.hash and wordlist:
    hashvalue = args.hash
    hash_funcs = {
        32: [lambda x: hashlib.md5(x)],
        40: [lambda x: hashlib.sha1(x)],
        64: [lambda x: hashlib.sha256(x)],
        96: [lambda x: hashlib.sha384(x)],
        128: [lambda x: hashlib.sha512(x)]
    }
    length = len(hashvalue)
    if length in hash_funcs:
        result = brute_force(hashvalue, hash_funcs[length], wordlist)
        if result:
            print(f'{good} Found: {result}')
        else:
            print(f'{bad} No match found.')
    else:
        print(f'{bad} Unsupported hash length.')
