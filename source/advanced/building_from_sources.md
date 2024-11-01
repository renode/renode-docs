# Building Renode from source

This document provides detailed information on how to prepare the build environment, and then build and test Renode itself.

## Prerequisites

### Core prerequisites

::::{tab} Linux

The following instructions have been tested on Ubuntu 22.04, however there should not be any major issues preventing you from using other (especially Debian-based) distributions as well.

:::{tab} Mono
First, install the `mono-complete` package as per the installation instructions for various Linux distributions which can be found on [the Mono project website](https://www.mono-project.com/download/stable/#download-lin).
:::

:::{tab} .NET
First, install the `.NET SDK` package as per the installation instructions, which can be found on [the official .NET site](https://dotnet.microsoft.com/en-us/download/dotnet/6.0).

:::{note}
Make sure to install the `6.0.4xx` branch (e.g. `6.0.427`) as otherwise the build will fail with a `NETSDK1100: Windows is required to build Windows desktop applications` error. On Ubuntu this requires using either the Microsoft package feed or installing manually
:::

:::

To install the remaining dependencies, use:

    sudo apt update
    sudo apt install git automake cmake autoconf libtool g++ coreutils policykit-1 \
                  libgtk2.0-dev uml-utilities gtk-sharp2 python3 python3-pip

::::

::::{tab} macOS

On macOS, the Mono package can be obtained by using [a download link on the Mono project website](https://download.mono-project.com/archive/mdk-latest-stable.pkg).

To install the remaining prerequisites, use:

    brew install binutils gnu-sed coreutils dialog cmake
    xcode-select --install

:::{note}
   This requires [homebrew](https://brew.sh/) to be installed in your system.
:::

::::


::::{tab} Windows

Building Renode on Windows is based on Cygwin and requires you to properly set up the system environment.

**Cygwin**

1. Download [Cygwin installer](https://cygwin.com/setup-x86_64.exe).
2. Install it with an additional module: `openssh`.

**Git**

1. Download and install `git` as a **native** application.
   You can get it from [the official website](https://git-scm.com/downloads).
   You can use either a regular installation or a portable version.
2. Ensure the installation directory (`C:\Program Files\Git` by default) is in the system `PATH` variable. The installer offers to install a subset of `git` tools in `PATH`, this is the recommended option.

:::{note}
Prior to cloning the repository on *Windows*, git has to be configured appropriately:

    git config --global core.autocrlf false
    git config --global core.symlinks true
:::

**Python 3**

1. Download and install **native** Windows Python 3 framework from [the Python website](https://www.python.org/downloads/).

:::{note}
   Do not use the module provided by `Cygwin`.
   If you have Cygwin's version of Python already installed, make sure that the native's version location is included at the beginning of Cygwin's PATH variable.
:::

2. Add location of the binaries (`C:\Program Files (x86)\Python38-32` for a 32-bit version of Python 3.8 by default) to the system `PATH` variable.

**MinGW**

1. Download `MinGW-w64 8.1.0` with the `x86_64` architecture, `win32` threads and `sjlj` exception handling from [the download site](https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/8.1.0/threads-win32/sjlj/x86_64-8.1.0-release-win32-sjlj-rt_v6-rev0.7z).
2. Extract the downloaded package and add its `mingw64\bin` directory (for example `C:\mingw-w64\x86_64-8.1.0-release-win32-sjlj-rt_v6-rev0\mingw64\bin`) to the system `PATH` variable.

**CMake**

1. Download `CMake` and install Windows CMake from [the CMake website](https://cmake.org/download/).
2. Ensure that the installation directory is in the system `PATH`. The installer will offer to do this for you

**C# build tools**

:::{tab} .NET Framework

1. Download [VS Build Tools 2019](https://aka.ms/vs/16/release/vs_BuildTools.exe).
2. Run the installer, select the *Visual Studio Build Tools 2019* product and click *Install* or *Modify*.
3. Switch to the *Individual components* pane and select:

   * *.NET Framework 4.6.2 targeting pack* in section *.NET*,
   * *NuGet targets and build tasks* in section *Code tools*.

4. Add the location of the binaries (`C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin\amd64` by default) to the system `PATH` variable.

:::

:::{tab} .NET

See [the official .NET site](https://dotnet.microsoft.com/en-us/download/dotnet/6.0) for instructions on how to install `.NET SDK`.

:::

::::

## Downloading the source code

Renode’s source code is available on GitHub:

    git clone https://github.com/renode/renode.git
    cd renode

Submodules will be automatically initialized and downloaded during the build process, so you do not need to do it at this point.

### Additional prerequisites (for Robot framework testing)

If you followed the instructions above, Python should be installed in your system.
Install the `pip` package manager and some additional modules to enable writing and running test cases with the Robot framework:

    python3 -m pip install -r tests/requirements.txt

## Building Renode

:::{note}
On Windows, the building process described in this section can only be executed in a Cygwin shell.
:::

:::{note}
When building Renode with `.NET`, remember to use `--net` switch (`./build.sh --net`).
:::

To build Renode, run:

    ./build.sh

There are some optional flags you can use:

    -c                                clean instead of building
    -d                                build in debug configuration
    -v                                verbose
    -p                                create packages after building
    -n                                create nightly packages after building
    -t                                create a portable package (experimental, Linux only)
    -s                                update submodules
    -b                                custom build properties file
    -o                                custom output directory
    --skip-fetch                      skip fetching submodules and additional resources
    --no-gui                          build with GUI disabled
    --force-net-framework-version     build against different version of .NET Framework than specified in the solution
    --net                             build with dotnet
    -B                                bundle target runtime (default value: linux-x64, requires --net, -t)
    --profile-build                   build optimized for tlib profiling

Additionally you can directly specify flags which will be passed to the build system after `--`.
For example, if you wanted to override the `CompilerPath` property you could use::

    ./build.sh -- p:CompilerPath=/path/to/gcc

You can also build `Renode.sln` from your IDE (like MonoDevelop or Visual Studio), but the `build.sh` script has to be run at least once.

## Creating packages

The build script can create native packages only, i.e., you must run it on Windows to create an `.msi` installer package, on Linux for `.deb`, `.rpm` and `.pkg.tar.xz` packages or on macOS for the `.dmg` image.

There is also a separate procedure to create [Conda](https://docs.conda.io/en/latest/) packages, described in a [dedicated README](https://github.com/renode/renode/tree/master/tools/packaging/conda).

### Prerequisites

Depending on the system, there may be some prerequisites for building Renode packages.

:::{tab} Linux

Run:

    sudo apt-get install ruby ruby-dev rpm 'bsdtar|libarchive-tools'
    sudo gem install fpm

:::

:::{tab} macOS

No additional prerequisites for macOS.

:::

::::{tab} Windows

:::{note}

On Windows 10, it is important to enable .NET 3.5 in the system before installing the WiX Toolset.

The packaging process described in this section can only be executed in a Cygwin shell.

:::

1. Download and install the [WiX Toolset installer](https://wixtoolset.org/releases/) (version at least 3.11).
2. Add the `zip` package to Cygwin.

::::

### Building

To build binary packages, run:

    ./build.sh -p

The packages will have a version assigned to them, defined by the contents of the `tools/version` file.

You can also build nightly packages with:

    ./build.sh -pn

This will append a date and a commit SHA to the output files.

### Location of packages

After completing successfully, the script will print the location of the files created:

:::{tab} Linux

`renode/output/packages/renode_<version>.{deb|rpm|tar.gz}`

:::

:::{tab} macOS

`renode/output/packages/renode_<version>.dmg`

:::

:::{tab} Windows

`renode/output/packages/renode_<version>.msi`

:::
