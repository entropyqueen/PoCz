#!/usr/bin/env python
#
#  BabyCrawler PoC
#  basic and simple uri crawler for web pages
#  by Ark, just4fun
#  feel free to share =)
#

import re
import random
import requests
import sys
import codecs

def main():

    if len(sys.argv) != 2:
        print("Usage: {} <start_uri>".format(sys.argv[0]))
        return 1

    target_list = [codecs.encode(sys.argv[1], 'utf-8').strip(b'/')]
    target_r = re.compile(b"(https?://[\w]+\.[\w\.\-_]+/?)")
    x = 0

    while True:
        try:

            print(target_list[x])
            data = requests.request("GET", target_list[x], timeout=1)

            for uri in target_r.findall(data.content):
                if uri.strip(b'/') not in target_list:
                    target_list.append(uri.strip(b'/'))
        except IndexError:
            print("No more uri.")
            break
        except:
            pass
        x += 1

    return 0

if __name__ == "__main__":
    exit(main())
