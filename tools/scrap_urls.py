#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
import os

try:
    from requests_futures.sessions import FuturesSession
    from concurrent.futures import ThreadPoolExecutor,wait, as_completed
except ImportError:
    print("[!] You'll need to pip install requests-futures for this tool.")
    sys.exit()

tick = {}

BANNER = '''
=====================
    APK scrapper
=====================
'''

def scrap_apk_pages(pages,category,threads=25):
    """
    Scrap 'https://apkpure.com/<category>?page=<pages>' root page to find
    individual APK pages
        -pages = number of pages to iterate
        -category = app(default), dating, finance, games, business, medical...
    """
    APK_pages=[]
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=threads))
    queue = {}

    for page in range(pages+1): # page starts from 1 not 0 
        # Just dump all async request into the "queue" dict
        queue[page] = session.get('https://apkpure.com/{}?page={}'.format(category,page))
       
    # Then, grab all the response from the queue
    for page in range(pages+1):
        response = queue[page].result()
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('div', attrs={'class':'category-template-down'})
        for result in results:
            url = "https://apkpure.com" + result.find('a')['href']
            APK_pages.append(url)

    print("[+] Total APKs found =" + str(len(APK_pages)))
    return APK_pages


def scrap_apk_downloadurls(APK_pages,threads=25):
    """
    Scrap an array of APK pages to extract download URLs
    """
    
    queue = {}
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=threads))
    print("[+] Scraping APK download link...")

    APK_records= []
    for url in (APK_pages):
        queue[url] = session.get(url, allow_redirects=False)

    for url in (APK_pages):
        response = queue[url].result()
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            flink = soup.find('a', attrs={'id':'download_link'})['href']
            filename = soup.find('span', attrs={'class':'file'})
            # e.g. <span class="file">Bigfoot_v1.0.126.2000_apkpure.com.apk 
            # <span class="fsize">(80.5 MB)</span></span>
            # remove the inner span tag <class='fsize'> to extract just filename
            filesize = filename.span.extract()
            fname = filename.text.replace(" ","")
            fsize = filesize.text[1:-1]
            APK_records.append((fname, fsize, flink))
            #print(fname)
        except:
            pass
            #print ("[-] There was an issue getting the next APK file! Moving on ...")

    print("[+] APK download urls scraped = {}".format(len(APK_records)))
    return APK_records

def download(url, fname):

    global tick

    out_dir = 'apk-downloads'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir) 

    # for downloading files asynchronously (we need to use regular requests
    # with multithreading capability as file writing is involved
    response = requests.get(url,stream=True)
    #response.raise_for_status() #check for 4xx or 5xx
    
    #pbar = progressbar.ProgressBar()
    content_length = int(response.headers['content-length'])

    #check if file has been previously downloaded
    if not os.path.exists(out_dir + '/' + fname):
        with open('{}/{}'.format(out_dir,fname), 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            print("[+] File {}/{} saved!".format(out_dir,fname))
    
    else: 
        print("file :{}/{} already exists! skipping ...".format(out_dir,fname))


    # Refresh a status message
    tick['current'] += 1
    sys.stdout.flush()
    sys.stdout.write("    {}/{} complete...".format(tick['current'],tick['total']))
    sys.stdout.write('\r')



def download_apk_files(APK_records,threads=25):
    """
    Takes the array with the following scheme and downloads the
    APK files.
    """
    global tick 
    futures = [] 
    queue = {}
    tick['total'] = len(APK_records)
    tick['current'] = 0


    executor = ThreadPoolExecutor(max_workers=threads) 

    
    print("[+] Initiating Downloads! Grab a coffee, this could take a while...")

    # First just send the requests in an async fashion with x amount of threads)
    for i in (range(len(APK_records))):
        fname = APK_records[i][0] # APK filename
        fsize = APK_records[i][1] # APK file size (MB)
        flink = APK_records[i][2] # APK download link
    
        future = executor.submit(download, flink, fname)
        futures.append(future)

    #for f in tqdm(as_completed(futures), total=len(futures)):  # progress bar not quite working
    #    pass
    wait(futures, timeout=None) # need this line to hold here until all futures are completed.

                
def execute(pages,category):
    """
    Function called by main program
    """
    print(BANNER)
    # default category = app
    # default pages = 1
    APK_pages = scrap_apk_pages(pages,category)
    APK_records = scrap_apk_downloadurls(APK_pages)
    download_apk_files(APK_records)
    return
