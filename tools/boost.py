#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys


def build_boost(
    boost_source_dir,
    boost_libraries,
    build_dir,
    install_dir,
    install_headers,
    target_cpu,
    is_debug,
    static_link_crt,
    boost_layout,
    boost_shared_library,
    boost_defines,
    boost_env,
    toolset
):
    build_dir = os.path.abspath(build_dir)
    install_dir = os.path.abspath(install_dir)
    include_dir = '' if install_headers else '--includedir=.'

    if len(boost_env) > 0:
        with open(boost_env, 'r') as f:
            env = f.read()
            for e in env.split('\0'):
                kv = e.strip().split('=', 2)
                if len(kv) >= 2:
                    os.environ[kv[0]] = kv[1]

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

    if len(toolset) > 0:
        toolset = 'toolset=msvc-' + str(float(toolset) / 10)

    defines = ''
    if len(boost_defines) > 0:
        defines = ' '.join(map(lambda item: 'define=%s' %
                               item, boost_defines.split(',')))

    action = 'install' if len(boost_libraries) > 0 else 'header'
    cflags = ''
    if sys.platform == 'linux':
        cflags = 'cflags=-fPIC cxxflags=-fPIC'
    cmd = '%s --build-dir=%s --prefix=%s %s address-model=%d %s %s variant=%s link=%s threading=multi runtime-link=%s %s %s %s %s' % (
        b2, build_dir, install_dir, include_dir, address_model, layout, libraries, variant, link, runtime_link, toolset, cflags, defines, action)

    print(cmd)
    os.system(cmd)


def main():
    [
        boost_source_dir,
        boost_libraries,
        build_dir,
        install_dir,
        install_headers,
        target_cpu,
        is_debug,
        static_link_crt,
        boost_layout,
        boost_shared_library,
        boost_defines,
        boost_env,
        toolset,
    ] = sys.argv[1:]

    build_boost(
        boost_source_dir,
        boost_libraries.strip(),
        build_dir,
        install_dir,
        install_headers == 'true',
        target_cpu,
        is_debug == 'true',
        static_link_crt == 'true',
        boost_layout,
        boost_shared_library == 'true',
        boost_defines.strip(),
        boost_env.strip(),
        toolset.strip(),
    )


if __name__ == '__main__':
    main()
