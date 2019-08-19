#!/usr/bin/env python3

"""
firebase_enum by sambal0x (github.com/sambal0x

Purpose: Identify open firebaseio databases for Android apps

Features/To Dos:
    - Brute force with wordlist including mutation
    - Find an easy way to extract APKs from the google play store or scrap from apkpure (APK files exposed the firebaseio database name)
    - Extra firebase names from Alexa top 10000 (possile code reuse from other projects)
"""

import os
import sys
import re
import argparse
from tools import scrap_urls,process,keyword_search

BANNER = \
'''
______ _          _                    _____                      
|  ___(_)        | |                  |  ___|                     
| |_   _ _ __ ___| |__   __ _ ___  ___| |__ _ __  _   _ _ __ ___  
|  _| | | '__/ _ \ '_ \ / _` / __|/ _ \  __| '_ \| | | | '_ ` _ \ 
| |   | | | |  __/ |_) | (_| \__ \  __/ |__| | | | |_| | | | | | |
\_|   |_|_|  \___|_.__/ \__,_|___/\___\____/_| |_|\__,_|_| |_| |_|
                                                                  
                                                                  
 github.com/sambal0x                                                                     
'''

def parse_arguments():
    """
    Handles user-passed parameters
    """
    desc = "Firebase enumeration tool"
    parser = argparse.ArgumentParser(description=desc)

    script_path = os.path.dirname(__file__)

    #Keyword can be given multiple times
    parser.add_argument('-k', '--keyword', type=str,
                        required=False,
                        help='Keyword. Can use argument multiple times.')


    #Use included mutation file by default, or let user provide one
    parser.add_argument('-m', '--mutations', type=str, action='store',
                        default=script_path + '/tools/fuzz.txt',
                        help='Mutation. Default: tools/fuzz.txt')

    # How many pages of APKpure to scrap for APK files
    parser.add_argument('-p', '--pages', type=int,
                        help='Number of APKpure.com pages to parse',
                        default=1)
    
    parser.add_argument('-c', '--category', type=str,
                        help='APK category list from APKpure.com',
                        default='app')

    parser.add_argument('-a', '--apkpure', action='store_true',
                        help='download APKs from apkpure.com')


    parser.add_argument('-t', '--threads', type=int, action='store',
                        help='number of threads for requests',
                        default=5)


    args = parser.parse_args()
    return args


def main():
    """ 
    Main program function
    """
    args = parse_arguments()
    print(BANNER)

    # check if keyword module is requested
    if args.keyword:
        keyword_search.execute(args.mutations, args.keyword, args.threads)

    # else check if apkpure module is requested
    elif args.apkpure:
        scrap_urls.execute(args.pages, args.category, args.threads)
        process.execute()

    
    
    print("[+] All done")

if __name__== '__main__':
    main()


