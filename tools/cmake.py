#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys


def cmake_build(
    cmake_root,
    cmake_options,
    build_dir,
    install_dir,
    target_cpu,
    is_debug,
    static_link_crt,
):
    config = 'debug' if is_debug else 'release'
    options = ''
    if sys.platform == 'win32':
        options += '-A %s ' % ('Win32' if target_cpu == 'x86' else 'x64')
        crt_link_flags = 'MultiThreaded%s%s' % (
            'Debug' if is_debug else '',
            '' if static_link_crt else 'DLL',
        )
        options += '-DCMAKE_MSVC_RUNTIME_LIBRARY=%s ' % (crt_link_flags,)
    elif sys.platform == 'darwin':
        options += '-DCMAKE_OSX_ARCHITECTURES=%s ' % 'i386' if target_cpu == 'x86' else 'x86_64'
    else:
        address_model = '-m32' if target_cpu == 'x86' else '-m64'
        options += '-DCMAKE_C_FLAGS_INIT=%s -DCMAKE_CXX_FLAGS_INIT=%s ' % (
            address_model, address_model)
    options += '-DCMAKE_INSTALL_PREFIX=%s ' % install_dir
    if len(cmake_options) > 0:
        options += ' '.join(map(lambda item: '-D' + item,
                            cmake_options.split(',')))
    config_cmd = 'cmake -S %s -B %s %s' % (
        cmake_root,
        build_dir,
        options,
    )
    build_cmd = 'cmake --build %s --config %s' % (build_dir, config)
    install_cmd = 'cmake --install %s --config %s --prefix %s' % (
        build_dir,
        config,
        install_dir,
    )
    for cmd in (config_cmd, build_cmd, install_cmd):
        print(cmd)
        sys.stdout.flush()
        os.system(cmd)


def main():
    [
        cmake_root,  # rebase_path(cmake_root, root_build_dir)
        cmake_options,  # string_join(",", cmake_options)
        # rebase_path(target_out_dir, root_build_dir) + "/$target_name"
        build_dir,
        # rebase_path(root_out_dir, root_build_dir) + "/$target_name"
        install_dir,
        target_cpu,  # "$target_cpu"
        is_debug,  # "$is_debug"
        static_link_crt,  # "$static_link_crt"
    ] = sys.argv[1:]

    cmake_build(
        cmake_root,
        cmake_options.strip(),
        build_dir,
        install_dir,
        target_cpu,
        is_debug == 'true',
        static_link_crt == 'true',
    )


if __name__ == '__main__':
    main()
