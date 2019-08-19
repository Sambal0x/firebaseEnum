# firebaseEnum
Purpose: Enumerate exposed firebase databases

## Features:
* Downloads APKs from APKpure.com and analyse Android files for misconfigured Firebase databasases
  * List of APKs based on categories, or
  * search for specific APK or search for keywords (to-do)
* Mutate a keyword to find exposed Firebase databases (to-do)
  * Could be useful for when searching for a specific company
* Use Alex top domains names to find exposed Firebase database (to-do)

**Usage**
```
python3 firebaseEnum.py [-h] [--apkpure] [-c finance] [-p 1]  
```

**Complete Usage Details**
```
usage: firebaseEnum.py [-h] [-k KEYWORD] [-m MUTATIONS] [-p PAGES]
                       [-c CATEGORY] [-a]

Firebase enumeration tool

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORD, --keyword KEYWORD
                        Keyword. Can use argument multiple times.
  -m MUTATIONS, --mutations MUTATIONS
                        Mutation. Default: tools/fuzz.txt
  -p PAGES, --pages PAGES
                        Number of APKpure.com pages to parse
  -c CATEGORY, --category CATEGORY
                        APK category list from APKpure.com
  -a, --apkpure         download APKs from apkpure.com

```

**Disclaimer: This tool is for educational purposes only!**
