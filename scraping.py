# A quick and dirty way to detect web changes
# based on https://www.adventuresintechland.com/detect-when-a-webpage-changes-with-python

import hashlib
import urllib3
import random
import time
import json

http = urllib3.PoolManager()

urls = [
    'url1'
    'url2'
    'url3'
    'url4'
]


# Sleeptime in seconds
sleeptime = 60

def getHash(url):
    
    randint = random.randint(0,3)

    userAgents = [
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
        'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00'
    ]

    res = http.request('GET', url, headers={'User-agent': userAgents[randint]})
    
    return hashlib.sha224(res.data).hexdigest()

# initial hashes 
hashes = list(map(getHash, urls))

# make a dictionary aka JSON Object for mongoDB to store urls and a count for the number of changes since t0
moreCounts = [0] * 5
BanksAndCounts = dict(zip(urls, moreCounts))

# infinite loop
while 1:
    # get the new hashes per iteration
    newHashes = [x if x == getHash(urls[ind]) else getHash(urls[ind]) for ind, x in enumerate(hashes)]
    # update the counter in BanksAndCounts Obj if the hashes have changed
    moreCounts = [ i+1 if j != k else i for i,j,k in zip(moreCounts, hashes, newHashes)]
    # update the hashes to make room for another newHashes in next iter
    # This way is cheap because we have both lists already and we just swap pointers 
    hashes = newHashes
    BanksAndCounts = dict(zip(urls, moreCounts))
    print(json.dumps(BanksAndCounts))
    time.sleep(sleeptime)

