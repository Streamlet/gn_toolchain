# gn 工具链

![](https://github.com/Streamlet/gn_toolchain/actions/workflows/windows.yml/badge.svg) ![](https://github.com/Streamlet/gn_toolchain/actions/workflows/linux.yml/badge.svg) ![](https://github.com/Streamlet/gn_toolchain/actions/workflows/macos.yml/badge.svg)
---
[(Here is the English Version)](README.md)

本项目旨在给出一个简单的、开箱即用的 gn 工具链配置，使得在 gn+ninja 构建系统下的跨平台编译变得更容易。

## 用法

1. 将本项目所有文件放置到您的项目根目录 ‘build’ 目录中。您可以根据您的需要选择以普通目录形式、submodule 形式、subtree 形式导入本项目，也可以依靠一些依赖处理系统导入本项目。

2. 在您的项目根目录建立 ‘.gn’ 文件，内容如下：

```gn
buildconfig = "//build/BUILDCONFIG.gn"
```

3. 按照 gn 规则给您的项目建立 ‘BUILD.gn’ 文件。

4. 运行 `gn gen out` 以及 `ninja -C out`，构建项目。

## 用例

见项目 [gn_toolchain_sample](../../../gn_toolchain_sample)。

## 获取 gn & ninja

* 从源代码编译
  * https://gn.googlesource.com/gn
  * git://github.com/ninja-build/ninja.git
* 从官方网站下载二进制包
  * https://gn.googlesource.com/gn/#getting-a-binary
  * https://ninja-build.org/
* 从包管理器获取，各包管理器的对应包名如下：
  * Mac
    * Homebrew：(无 gn)、ninja
    * MacPorts：gn-devel、ninja
  * Linux
    * apt-get & apt：generate-ninja、ninja-build
    * yum & dnf：gn、ninja-build
    * pacman：gn、ninja
