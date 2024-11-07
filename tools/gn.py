#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys


def gn_build(
    root_dir,
    out_dir,
    targets,
    args
):
    gen_cmd = 'gn gen --root=%s %s --args="%s"' % (
        root_dir,
        out_dir,
        args.replace('"', '\\"')
    )
    build_cmd = 'ninja -C %s %s' % (out_dir, targets)
    for cmd in (gen_cmd, build_cmd):
        print(cmd)
        sys.stdout.flush()
        r = os.system(cmd)
        assert r == 0


def main():
    [
        root_dir,
        out_dir,
        targets,
        args,
    ] = sys.argv[1:]

    gn_build(
        root_dir,
        out_dir,
        targets.strip(),
        args.strip()
    )


if __name__ == '__main__':
    main()
