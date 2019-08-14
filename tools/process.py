#!/usr/bin/env python3

import os
import csv
import requests
import subprocess
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor,wait, as_completed

BANNER = '''
======================
 Firebase Enumeration
======================
'''

def get_firebase_urls(apk_folder):
    """
    Extract firebase urls in a folder of APKs
    """
    print("Looking for firebase URLS in {}".format(apk_folder))

    #os.chdir(apk_folder)

    with open('firebaseio.csv','w') as csv_file:
        #fieldnames = ['firebase_url','source']
        csv_writer = csv.writer(csv_file, delimiter=',')
        #csv_writer.writeheader()
        #print(os.listdir(apk_folder))

        for filename in os.listdir(apk_folder):            
            raw=[] 
            clean=[]
            # Found it is quicker to string than extract with apktool
            cmd = ("strings {}/{} | grep -aihoE 'https://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*.firebaseio.com'".format(apk_folder,filename))
            temp = subprocess.run(cmd,
                                            shell=True, capture_output=True,text=True) # need to not use Shell=True for security reasons
            raw.append(temp.stdout)
            clean=raw[0].split("\n")
            for firebase_url in clean:
                if firebase_url: #check if not empty , especially the last element in array
                    csv_writer.writerow([firebase_url,filename])



def check_open_database(f_file,threads=5):
    """
    Takes a list of firebase urls and check for if its open
    """
    print("[+] Checking for open firebase databases...")

    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=threads))
    queue = {}
    urls = []
    
    with open (f_file, 'r') as filehandler:
        lines = filehandler.read().splitlines() #need to remove \r\n from each line
        for line in lines:
            url = (line.split(",")[0].strip()) #Gets the clean url        
            try:
                queue[url] = session.get(url+ '/.json')
                #print('{} done!'.format(url))
            except OSError:
                print("[!] Connection error on {}".format(url))

        for line in lines:
            url = (line.split(",")[0].strip())
            source = (line.split(",")[1].strip())
            try:
                response = queue[url].result()
                #print(response.status_code)
                if response.status_code == 200:
                    print('[+] {}/.json is vulnerable'.format(url))
                    print('         [source] : {}'.format(source))
            except OSError:
                print("[!] Error on {}".format(url))

'''
    for url in urls:
         Just dump all sync request into the 'queue' dict
        try:
            queue[url] = session.get(url+ '/.json')
            #print('{} done!'.format(url))
        except OSError:
            print("[!] Connection error on {}".format(url))
            
    # Then, grab all hte response from the queue
    for url in urls:
        #print('checking {}'.format(url))
        try:
            response = queue[url].result()
            print(response.status_code)
            if response.status_code == 200:
                print('[+] {}/.json is vulnerable'.format(url))
        except OSError:
            print("[!] Error on {}".format(url))
'''
        
                
def execute():
    """
    Function called by main program
    """

    print(BANNER)
    get_firebase_urls('/root/Dev/firebaseEnum/apk-downloads/')
    check_open_database('firebaseio.csv')
    return
