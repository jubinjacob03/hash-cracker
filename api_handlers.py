import warnings
import requests
import re

# Suppress only the single InsecureRequestWarning from urllib3 needed
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Define API handlers
def alpha(hashvalue, hashtype):
    return False

def beta(hashvalue, hashtype):
    response = requests.get(f'https://hashtoolkit.com/reverse-hash/?hash={hashvalue}').text
    match = re.search(r'/generate-hash/\?text=(.*?)"', response)
    return match.group(1) if match else False

def gamma(hashvalue, hashtype):
    response = requests.get(f'https://www.nitrxgen.net/md5db/{hashvalue}', verify=False).text
    return response if response else False

def delta(hashvalue, hashtype):
    return False

def theta(hashvalue, hashtype):
    response = requests.get(f'https://md5decrypt.net/Api/api.php?hash={hashvalue}&hash_type={hashtype}&email=your_email@domain.com&code=your_api_code').text
    return response if len(response) != 0 else False

def crackstation(hashvalue):
    response = requests.post(
        'https://crackstation.net/',
        data={'hashes': hashvalue, 'decrypt': 'Crack Hashes!'}
    ).text
    match = re.search(r'Hash result: <b>(.*?)</b>', response)
    return match.group(1) if match else False

def hashes_org(hashvalue):
    response = requests.get(f'https://hashes.org/api.php?hash={hashvalue}').json()
    if response['result'] == 'found':
        return response['plain']
    return False
