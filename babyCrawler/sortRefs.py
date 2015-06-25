#!/usr/bin/env python2
#
#  BabyCrawler PoC
#  Real time referencer, crawl uris and sort them in order of reference
#  by Ark, just4fun
#  feel free to share =)
#

import re
import random
import requests
import sys

def main() :

    if len(sys.argv) != 2 :
        print("Usage: {} <start_uri>".format(sys.argv[0]))
        return 1

    target_list = [[sys.argv[1].strip('/'), 1]]
    target_r = re.compile("href=[\"']([a-z]+://[a-z0-9\.\-_]+/?)[\"']")
    x = 0

    while True :
        try :
            top10 = sorted(target_list, key=lambda targets: targets[1], reverse=True)[:10]
            print("------------------------------------")
            for i in range(len(top10)) :
                print("{} - {} ({})".format(i, top10[i][0], top10[i][1]))
            data = requests.request("GET", target_list[x][0], verify=False, timeout=1)
            for uri in target_r.findall(data.content) :
                try :
                    next((y for y in target_list if y[0] == uri.strip('/')))[1] += 1
                except :
                    target_list.append([uri.strip('/'), 1])
        except IndexError :
            print "No more uri."
            return 0
        except :
            pass
        x += 1

    return 0
        

if __name__ == "__main__" :
    exit(main())
