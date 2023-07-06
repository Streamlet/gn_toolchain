#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys


def build_boost(
    boost_source_dir,
    boost_libraries,
    build_dir,
    install_dir,
    target_cpu,
    is_debug,
    static_link_crt,
    boost_layout,
    boost_shared_library,
):
    build_dir = os.path.abspath(build_dir, boost_source_dir)
    install_dir = os.path.abspath(install_dir, boost_source_dir)
    os.chdir(boost_source_dir)

    b2 = 'b2.exe' if sys.platform == 'win32' else './b2'
    if not os.path.exists(b2):
        if sys.platform == 'win32':
            os.system('bootstrap.bat')
        else:
            os.system('./bootstrap.sh')
    runtime_link = 'static' if sys.platform == 'win32' and static_link_crt else 'shared'
    address_model = 32 if target_cpu == 'x86' else 64
    variant = 'debug' if is_debug else 'release'
    libraries = ''
    if len(boost_libraries) > 0:
        libraries = ' '.join(
            map(lambda item: '--with-' + item, boost_libraries.split(',')))
    layout = ''
    link = 'shared' if boost_shared_library else 'static'
    if len(boost_layout) > 0:
        layout = '--layout=%s' % boost_layout
    action = 'install' if len(boost_libraries) > 0 else 'header'
    cflags = ''
    if sys.platform == 'linux':
        cflags = 'cflags=-fPIC cxxflags=-fPIC'
    cmd = '%s --build-dir=%s --prefix=%s address-model=%d %s %s variant=%s link=%s threading=multi runtime-link=%s %s %s' % (
        b2, build_dir, install_dir, address_model, layout, libraries, variant, link, runtime_link, cflags, action)

    print(cmd)
    os.system(cmd)


def main():
    [
        boost_source_dir,  # rebase_path(boost_source_dir, root_build_dir)
        boost_libraries,  # string_join(",", boost_libraries)
        # rebase_path(target_out_dir, root_build_dir) + "/$target_name"
        build_dir,
        # rebase_path(root_out_dir, root_build_dir) + "/$target_name"
        install_dir,
        target_cpu,  # "$target_cpu"
        is_debug,  # "$is_debug"
        static_link_crt,  # "$static_link_crt"
        boost_layout,  # "$boost_layout"
        boost_shared_library,  # "$boost_shared_library"
    ] = sys.argv[1:]

    build_boost(
        boost_source_dir,
        boost_libraries.strip(),
        build_dir,
        install_dir,
        target_cpu,
        is_debug == 'true',
        static_link_crt == 'true',
        boost_layout,
        boost_shared_library == 'true',
    )


if __name__ == '__main__':
    main()
