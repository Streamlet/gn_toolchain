#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import psutil


def makefile_build(
    makefile_root_dir,
    makefile_config_cmd,
    makefile_prefix,
    makefile_config_options,
    makefile_file,
    makefile_options,
    makefile_targets,
    makefile_env,
):
    prefix = os.path.abspath(makefile_prefix)
    env = os.path.abspath(makefile_env)
    config_options = ''
    if len(makefile_config_options) > 0:
        config_options = ' '.join(
            map(lambda item: item, makefile_config_options.split(',')))
    options = ''
    if len(makefile_options) > 0:
        options = ' '.join(map(lambda item: item, makefile_options.split(',')))
    targets = []
    if len(makefile_targets) > 0:
        targets = makefile_targets.split(',')
    else:
        targets = ['']

    os.chdir(makefile_root_dir)
    if len(makefile_config_cmd) > 0:
        config_cmd = '%s --prefix=%s %s' % (
            makefile_config_cmd,
            prefix,
            config_options,
        )
        print(config_cmd)
        sys.stdout.flush()
        os.system(config_cmd)
        os.system('echo > "%s"' % os.path.join(prefix, 'configure'))

    ninja_path = psutil.Process(os.getppid()).exe()
    make = 'make' if sys.platform != 'win32' else (
        '%s -t msvc -e %s -- nmake' % (ninja_path, env))
    if sys.platform == 'win32' and len(makefile_file) > 0:
        make += " /f %s" % makefile_file
    for target in targets:
        make_cmd = '%s %s %s' % (make, target, options)
        print(make_cmd)
        sys.stdout.flush()
        os.system(make_cmd)
        os.system('echo > "%s"' % os.path.join(prefix, 'make'
                                               + ('' if len(target) == 0 else '_' + target.replace('/', '_').replace('\\', '_').replace('.', '_'))))


def main():
    [
        makefile_root_dir,  # rebase_path(makefile_root_dir, root_build_dir)
        makefile_config_cmd,  # "$makefile_config_cmd "
        makefile_prefix,  # rebase_path(makefile_prefix, root_build_dir)
        # string_join(",", makefile_config_options) + " "
        makefile_config_options,
        makefile_file,  # makefile_file + " "
        makefile_options,  # string_join(",", makefile_options) + " "
        makefile_targets,  # string_join(",", makefile_target) + " "
        makefile_env,  # makefile_env + " "
    ] = sys.argv[1:]

    makefile_build(
        makefile_root_dir,
        makefile_config_cmd.strip(),
        makefile_prefix,
        makefile_config_options,
        makefile_file.strip(),
        makefile_options.strip(),
        makefile_targets.strip(),
        makefile_env.strip(),
    )


if __name__ == '__main__':
    main()
