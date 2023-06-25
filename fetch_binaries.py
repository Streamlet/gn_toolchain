#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import zipfile
import stat
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
    url = {}
    if sys.platform == 'win32':
        url['gn'] = 'https://chrome-infra-packages.appspot.com/dl/gn/gn/windows-amd64/+/latest'
        url['ninja'] = 'https://github.com/ninja-build/ninja/releases/download/%s/ninja-win.zip' % ninja_latest
    elif sys.platform == 'darwin':
        url['gn'] = 'https://chrome-infra-packages.appspot.com/dl/gn/gn/mac-amd64/+/latest'
        url['ninja'] = 'https://github.com/ninja-build/ninja/releases/download/%s/ninja-mac.zip' % ninja_latest
    elif sys.platform == 'linux':
        url['gn'] = 'https://chrome-infra-packages.appspot.com/dl/gn/gn/linux-amd64/+/latest'
        url['ninja'] = 'https://github.com/ninja-build/ninja/releases/download/%s/ninja-linux.zip' % ninja_latest
    else:
        assert False, 'Unsupport system: %s' % sys.platform

    for t in ('gn', 'ninja',):
        z = os.path.join('bin', t + '.zip')
        download(url[t], z)
        with zipfile.ZipFile(z, 'r') as zip:
            f = t + '.exe' if sys.platform == 'win32' else t
            zip.extract(f, 'bin')
            if sys.platform != 'win32':
                p = os.path.join('bin', f)
                st = os.stat(p)
                os.chmod(p, st.st_mode | stat.S_IEXEC)
        os.remove(z)


if __name__ == '__main__':
    main()
