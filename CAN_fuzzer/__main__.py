#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import multiprocessing
import itertools
import string
import subprocess
from functools import partial

charset = __import__('string').ascii_uppercase
num_parts = 4
part_size = len(charset) // num_parts

def do_job(data, repeat):

    permutations = [charset] * repeat

    for x in itertools.product(data, *permutations):
        try:
            #generate a random bus id
            bus_id = hex(random.randint(0, 0xFFF))[2:].rjust(3, '0').upper()
            #send frame to CAN
            subprocess.call(('cansend', 'vircar', '%s#%s' %(bus_id, "".join([hex(ord(x))[2:] for x in "".join(x)]))))
        except Exception as e:
            print(e)
            raise

if __name__ == '__main__':

    for x in range(8):
        pool = multiprocessing.Pool(processes=num_parts)
        parts = []
        for i in range(num_parts):
            if i == num_parts - 1:
                parts.append(charset[part_size * i :])
            else:
                parts.append(charset[part_size * i : part_size * (i+1)])

        pool.map_async(partial(do_job, repeat=x), parts)
        pool.close()
        pool.join()

