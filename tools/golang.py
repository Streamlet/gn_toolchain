#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys


def golang_build(go_root_dir, go_out_dir, go_gcflags, go_ldflags, is_debug):
    out_dir = os.path.abspath(go_out_dir)
    gcflags_list = []
    if len(go_gcflags) > 0:
        gcflags_list = go_gcflags.split(',')
    if is_debug:
        gcflags_list = gcflags_list + ['-N', '-l']
    gcflags = ' '.join(gcflags_list)
    if len(gcflags) > 0:
        gcflags = ' -gcflags "%s"' % gcflags

    ldlags_list = []
    if len(go_ldflags) > 0:
        ldlags_list = go_ldflags.split(',')
    if not is_debug:
        ldlags_list = ldlags_list + ['-w', '-s']
    ldflags = ' '.join(ldlags_list)
    if len(ldflags) > 0:
        ldflags = ' -ldflags "%s"' % ldflags

    os.chdir(go_root_dir)

    cmd = 'go build%s%s -o %s' % (gcflags, ldflags, out_dir)
    print(cmd)
    os.system(cmd)


def main():
    [
        go_root_dir,
        go_out_dir,
        go_gcflags,
        go_ldflags,
        is_debug,
    ] = sys.argv[1:]

    golang_build(
        go_root_dir,
        go_out_dir,
        go_gcflags.strip(),
        go_ldflags.strip(),
        is_debug == 'true',
    )


if __name__ == '__main__':
    main()
