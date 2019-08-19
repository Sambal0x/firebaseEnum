# firebaseEnum
Purpose: Enumerate exposed firebase databases

## Features:
* Downloads APKs from APKpure.com and analyse Android files for misconfigured Firebase databasases
  * List of APKs based on categories, or
  * search for specific APK or search for keywords (to-do)
* Mutate a keyword to find exposed Firebase databases (to-do)
  * Could be useful for when searching for a specific company

**Usage**
```
python3 firebaseEnum.py [-h] [--apkpure] [-c] [-p] [k]
```

**Example**

Downloads 2 pages of finance related Android apps from APKpure.com and check for exposed firebase databases
```
python3 firebaseEnum.py -a -c finance -p 2
```

Search for possible `company` related firebase open databases for analysis
```
python3 firebaseEnum.py -k company
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
  -a, --apkpure         enable APKpure.com module

```

**Disclaimer: This tool is for educational purposes only!**
