#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import zipfile
if sys.version >= '3':
    import urllib.request as urllib
else:
    import urllib


def get_redirected_url(url):
    try:
        remote = urllib.urlopen(url)
    except Exception as e:
        print(e)
        return None
    return remote.url


def download(url, file):
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    try:
        remote = urllib.urlopen(url)
    except Exception as e:
        print(e)
        return False
    with open(file, 'wb') as local:
        BLOCK_SIZE = 1024 * 1024
        while True:
            buffer = remote.read(BLOCK_SIZE)
            local.write(buffer)
            if len(buffer) < BLOCK_SIZE:
                break
    return True


def main():
    os.chdir(os.path.dirname(__file__))

    ninja_latest = os.path.basename(get_redirected_url(
        'https://github.com/ninja-build/ninja/releases/latest'))
    if sys.platform == 'win32':
        gn_url = 'https://chrome-infra-packages.appspot.com/dl/gn/gn/windows-amd64/+/latest'
        ninja_url = 'https://github.com/ninja-build/ninja/releases/download/%s/ninja-win.zip' % ninja_latest
    elif sys.platform == 'darwin':
        gn_url = 'https://chrome-infra-packages.appspot.com/dl/gn/gn/mac-amd64/+/latest'
        ninja_url = 'https://github.com/ninja-build/ninja/releases/download/%s/ninja-mac.zip' % ninja_latest
    elif sys.platform == 'linux':
        gn_url = 'https://chrome-infra-packages.appspot.com/dl/gn/gn/linux-amd64/+/latest'
        ninja_url = 'https://github.com/ninja-build/ninja/releases/download/%s/ninja-linux.zip' % ninja_latest
    else:
        assert False, 'Unsupport system: %s' % sys.platform

    gn_zip = os.path.join('bin', 'gn.zip')
    ninja_zip = os.path.join('bin', 'ninja.zip')

    download(gn_url, gn_zip)
    with zipfile.ZipFile(gn_zip, 'r') as zip:
        zip.extractall('bin')
    os.remove(gn_zip)

    download(ninja_url, ninja_zip)
    with zipfile.ZipFile(ninja_zip, 'r') as zip:
        zip.extractall('bin')
    os.remove(ninja_zip)


if __name__ == '__main__':
    main()
