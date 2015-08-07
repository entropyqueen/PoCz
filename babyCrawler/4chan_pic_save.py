#!/usr/bin/env python
#
# Simple script to save all pics from a thread on 4chan.
# feel free to share.
# WTFPL LICENSE
# By ark.
#

import re
import requests
import sys
import os

def main():

    if len(sys.argv) != 3:
        print("Usage: {} <thread url> <folder>".format(sys.argv[0]))
        return 1

    thread = sys.argv[1]
    if not '4chan.org' in thread:
        return 1

    directory = sys.argv[2]
    board = re.findall('https://boards.4chan.org/([\w]+)/thread/633183511', thread)
    img_r = re.compile(b'<a href="//i.4cdn.org/{}/([\d]+\.[\w]+)"'.format(board))

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    data = requests.get(thread, timeout=1)
    for x in img_r.findall(data.content):
        with open(directory + '/' + os.fsdecode(x), 'wb') as f:
            img = requests.get(b'https://i.4cdn.org/{}/'.format(board) + x)
            f.write(img.content)
    
    return 0

if __name__ == "__main__":
    exit(main())
