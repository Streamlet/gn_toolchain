# gn toolchain

![](https://github.com/Streamlet/gn_toolchain/actions/workflows/windows.yml/badge.svg) ![](https://github.com/Streamlet/gn_toolchain/actions/workflows/linux.yml/badge.svg) ![](https://github.com/Streamlet/gn_toolchain/actions/workflows/macos.yml/badge.svg)
---
[（中文版本见这里）](README_zh.md)

This project provides a simple and out-of-the-box gn toolchain configuration, to make cross-platform compile easier under the gn+ninja build system.

## Usage

1. Put all files of this project into 'build' directory in the root of your project. You could import this project in the form of ordinary folder, submuodule, subtree, or though some dependency manager system, as you wish.

2. Create a '.gn' file in the root directory, with content as following：

```gn
buildconfig = "//build/BUILDCONFIG.gn"
```

3. Write your 'BUILD.gn' files for your project, following the rules of gn.

4. Run `gn gen out` and `ninja -C out`, to build your project.

## Sample

Please refer to project [gn_toolchain_sample](../../../gn_toolchain_sample).

## Fetch gn & ninja

* Build from source code
  * https://gn.googlesource.com/gn
  * git://github.com/ninja-build/ninja.git
* Download binaries from official website
  * https://gn.googlesource.com/gn/#getting-a-binary
  * https://ninja-build.org/
* Get from package manager. Try package names as following:
  * Mac
    * Homebrew: (no gn), ninja
    * MacPorts: gn-devel, ninja
  * Linux
    * apt-get & apt: generate-ninja, ninja-build
    * yum & dnf: gn, ninja-build
    * pacman: gn, ninja
