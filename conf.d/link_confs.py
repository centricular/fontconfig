#!/usr/bin/env python3

import os
import sys
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('availpath')
    parser.add_argument('confpath')
    parser.add_argument('links', nargs='+')
    args = parser.parse_args()

    if not os.path.exists(args.confpath):
        os.makedirs(args.confpath)

    for link in args.links:
        src = os.path.join(args.availpath, link)
        dst = os.path.join(args.confpath, link)
        try:
            os.symlink(src, dst)
        except NotImplementedError:
            break
        except FileExistsError:
            pass
