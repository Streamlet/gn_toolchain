#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys


def makefile_build(
    makefile_root_dir,
    makefile_config_cmd,
    makefile_prefix,
    makefile_options,
    makefile_targets,
):
    prefix = os.path.abspath(makefile_prefix)
    options = ""
    if len(makefile_options) > 0:
        options = " ".join(map(lambda item: item, makefile_options.split(",")))
    targets = [""]
    if len(makefile_targets) > 0:
        targets = makefile_targets.split(",")

    os.chdir(makefile_root_dir)

    config_cmd = "%s --prefix=%s %s" % (
        makefile_config_cmd,
        prefix,
        options,
    )
    print(config_cmd)
    sys.stdout.flush()
    os.system(config_cmd)
    os.system('touch "%s"' % os.path.join(prefix, "configure"))

    for target in targets:
        make_cmd = "make %s" % target
        print(make_cmd)
        sys.stdout.flush()
        os.system(make_cmd)
        os.system('touch "%s"' % os.path.join(prefix, "make" +
                  ("" if len(target) == 0 else "_"+target.replace(os.path.sep, '_'))))


def main():
    [
        makefile_root_dir,  # rebase_path(makefile_root_dir, root_build_dir),
        makefile_config_cmd,  # "$makefile_config_cmd"
        makefile_prefix,  # rebase_path(makefile_prefix, root_build_dir),
        makefile_options,  # string_join(",", makefile_options) + " ",
        makefile_targets,  # string_join(",", makefile_target) + " ",
    ] = sys.argv[1:]

    makefile_build(
        makefile_root_dir,
        makefile_config_cmd,
        makefile_prefix,
        makefile_options.strip(),
        makefile_targets.strip(),
    )


if __name__ == "__main__":
    main()
