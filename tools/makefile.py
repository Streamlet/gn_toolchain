#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys


def makefile_build(
    makefile_root_dir,
    makefile_config_cmd,
    makefile_prefix,
    makefile_options,
    makefile_target,
):
    prefix = os.path.abspath(makefile_prefix)
    options = ""
    if len(makefile_options) > 0:
        options = " ".join(map(lambda item: item, makefile_options.split(",")))
    target = ""
    if len(makefile_target) > 0:
        target = " ".join(map(lambda item: item, makefile_target.split(",")))

    os.chdir(makefile_root_dir)

    config_cmd = "%s --prefix=%s %s" % (
        makefile_config_cmd,
        prefix,
        options,
    )
    build_cmd = "make %s" % target
    install_cmd = "make install"
    for cmd in (config_cmd, build_cmd, install_cmd):
        print(cmd)
        sys.stdout.flush()
        os.system(cmd)


def main():
    [
        makefile_root_dir, # rebase_path(makefile_root_dir, root_build_dir),
        makefile_config_cmd, # "$makefile_config_cmd"
        makefile_prefix, # rebase_path(makefile_prefix, root_build_dir),
        makefile_options, # string_join(",", makefile_options) + " ",
        makefile_target, # string_join(",", makefile_target) + " ",
    ] = sys.argv[1:]

    makefile_build(
        makefile_root_dir,
        makefile_config_cmd,
        makefile_prefix,
        makefile_options.strip(),
        makefile_target.strip(),
    )


if __name__ == "__main__":
    main()
