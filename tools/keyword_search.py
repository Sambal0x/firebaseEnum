#!/usr/bin/env python3

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
    queue = {}
    
    for name in names:
        # Just dump all sync request into the 'queue' dict
        try:
            url = ('https://' + name + '.firebaseio.com/.json')
            queue[name] = session.get(url)
            #print('{} done!'.format(name))
        except OSError:
            print("[!] Connection error on {}".format(name))
            
    # Then, grab all hte response from the queue
    for name in names:
        try:
            url = ('https://' + name + '.firebaseio.com/.json')
            response = queue[name].result()

            # Refresh a status message
            tick['current'] += 1
            sys.stdout.flush()
            sys.stdout.write("    {}/{} complete...".format(tick['current'],tick['total']))
            sys.stdout.write('\r')
            if response.status_code == 200:
                print('[+] {} is vulnerable'.format(url))
        except OSError:
            print("[!] Error in getting response from {}".format(url))

    # clear status message 
    sys.stdout.write('\r')

        
                
def execute(mutation_file,keyword):
    """
    Function called by main program
    """

    print(BANNER)
    mutations = read_mutations(mutation_file)
    names = build_names(keyword, mutations)
    check_open_database_keyword(names)
    return
