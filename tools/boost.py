#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys


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
    build_dir = os.path.relpath(build_dir, boost_source_dir)
    install_dir = os.path.relpath(install_dir, boost_source_dir)
    os.chdir(boost_source_dir)

    b2 = "b2.exe" if sys.platform == "win32" else "./b2"
    if not os.path.exists(b2):
        if sys.platform == "win32":
            os.system("bootstrap.bat")
        else:
            os.system("./bootstrap.sh")
    runtime_link = "static" if static_link_crt else "dynamic"
    address_model = 32 if target_cpu == "x86" else 64
    variant = "debug" if is_debug else "release"
    libraries = ""
    if len(boost_libraries) > 0:
        libraries = " ".join(
            map(lambda item: "--with-" + item, boost_libraries.split(","))
        )
    layout = ''
    link = 'shared' if boost_shared_library else 'static'
    if (len(boost_layout) > 0):
        layout = "--layout=%s" % boost_layout
    action = "install" if len(boost_libraries) > 0 else "header"
    cmd = (
        "%s --build-dir=%s --prefix=%s address-model=%d %s %s variant=%s link=%s threading=multi runtime-link=%s %s"
        % (
            b2,
            build_dir,
            install_dir,
            address_model,
            layout,
            libraries,
            variant,
            link,
            runtime_link,
            action,
        )
    )
    print(cmd)
    os.system(cmd)


def main():
    [
        boost_source_dir,  # rebase_path(boost_source_dir, root_build_dir)
        boost_libraries,  # string_join(",", boost_libraries)
        build_dir,  # rebase_path(target_out_dir, root_build_dir) + "/$target_name"
        install_dir,  # rebase_path(root_out_dir, root_build_dir) + "/$target_name"
        target_cpu,  # "$target_cpu"
        is_debug,  # "$is_debug"
        static_link_crt,  # "$static_link_crt"
        boost_layout, # "$boost_layout"
        boost_shared_library # "$boost_shared_library"
    ] = sys.argv[1:]

    build_boost(
        boost_source_dir,
        boost_libraries.strip(),
        build_dir,
        install_dir,
        target_cpu,
        is_debug == "true",
        static_link_crt == "true",
        boost_layout,
        boost_shared_library == "true"
    )


if __name__ == "__main__":
    main()
