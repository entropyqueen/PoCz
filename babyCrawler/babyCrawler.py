#!/usr/bin/env python
#
#  BabyCrawler PoC
#  by Ark, just4fun
#  feel free to share =)
#

import re
import requests
import sys

def process(target, old_targets, target_r) :

    try :
        data = requests.request("GET", target, verify=False)
    except :
        return # if we fail, let's move on, there is plenty of stuff to discover anyway!
    uris = target_r.findall(data.content)
    print("{}".format(target))

    for uri in uris :
        if uri not in old_targets:
            old_targets.append(uri)
            process(uri, old_targets, target_r)

def main() :

    if len(sys.argv) != 2 :
        print("Usage: {} <start_uri>".format(sys.argv[0]))
        return 1

    target = sys.argv[1]
    old_targets = [target]
    target_r = re.compile("(https?://[a-z0-9\.\-_]+/?)")

    process(target, old_targets, target_r)

    print("No new uri found")
    return 0
        

if __name__ == "__main__" :
    exit(main())
