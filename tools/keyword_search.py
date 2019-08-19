#!/usr/bin/env python3

import re
import os
import sys
import csv
import requests
import subprocess
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor,wait, as_completed

BANNER = '''
==========================
 Keyword based Enumeration
==========================
'''

def read_mutations(mutation_file):
    """
    Read mutations file into memory for processing
    """
    with open(mutation_file, encoding="utf8", errors="ignore") as infile:
        mutations = infile.read().splitlines()

    print("[+] Mutations list imported: {} items".format(len(mutations)))
    return mutations


def build_names(keyword, mutations):
    """
    Combine base and mutations for processing
    """
    names = []

    # first, include with no mutation
    names.append(keyword)
    for mutation in mutations:
        # Clense word to avoid bad characters
        mutation = clean_text(mutation)

        # Appends
        names.append("{}{}".format(keyword, mutation))
        names.append("{}-{}".format(keyword, mutation))

        # Prepends
        names.append("{}{}".format(mutation, keyword))
        names.append("{}-{}".format(mutation, keyword))

    print("[+] Mutated results: {} items".format(len(names)))

    return names


def check_open_database_keyword(names,threads=5):
    """
    Takes a list of firebase names and check if its exposed
    """
    print("[+] Checking for open firebase databases...")

    tick = {}
    tick['total'] = len(names)
    tick['current'] = 0

    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=threads))
   
     # Break the url list into smaller lists based on thread size
    batches = [names[x:x+threads] for x in range(0, len(names), threads)]

    for batch in batches:
        queue = {}
        for name in batch:
            # Just dump all sync request into the 'queue' dict
            try:
                url = ('https://' + name + '.firebaseio.com/.json')
                queue[name] = session.get(url)
                #print('{} done!'.format(name))
            except OSError:
                print("[!] Connection error on {}".format(name))
            
        # Then, grab all hte response from the queue
        for name in batch:
            try:
                #print('{} grabbing response!'.format(name))
                url = ('https://' + name + '.firebaseio.com/.json')
                response = queue[name].result()

                if response.status_code == 200:
                    print('[+] {} is vulnerable'.format(url))
            except OSError:
                print("[!] Error in getting response from {}".format(url))

            # Refresh a status message
            tick['current'] += 1
            sys.stdout.flush()
            sys.stdout.write("    {}/{} complete...".format(tick['current'],tick['total']))
            sys.stdout.write('\r')

def clean_text(text):
    """
    Clean text to be RFC compliant for hostnames / DNS
    """
    banned_chars = re.compile('[^a-z0-9]')
    text_lower = text.lower()
    text_clean = banned_chars.sub('', text_lower)

    return text_clean

                
def execute(mutation_file,keyword, threads):
    """
    Function called by main program
    """

    print(BANNER)
    mutations = read_mutations(mutation_file)
    names = build_names(keyword, mutations)
    check_open_database_keyword(names, threads)
    return
