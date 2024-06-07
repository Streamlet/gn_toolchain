#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys

def main():
    if sys.platform == 'win32':
        os.system("copy /Y %s %s" % (sys.argv[1].replace('/', os.path.sep), sys.argv[2].replace('/', os.path.sep)))
    else:
        os.system("cp -r %s %s" % (sys.argv[1], sys.argv[2]))

if __name__ == '__main__':
    main()
