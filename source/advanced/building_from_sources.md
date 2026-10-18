# Building Renode from source

This document provides detailed information on how to prepare the build environment, and then build and test Renode itself.

## Prerequisites

### Core prerequisites

::::{tab} Linux

The following instructions have been tested on Ubuntu 24.04, however there should not be any major issues preventing you from using other (especially Debian-based) distributions as well.

First, install the `.NET SDK` package as per the installation instructions, which can be found on [the official .NET site](https://dotnet.microsoft.com/en-us/download/dotnet/8.0).

To install the remaining dependencies, use:

    sudo apt update
    sudo apt install git automake cmake autoconf libtool g++ coreutils policykit-1 \
                  libgtk-3-dev uml-utilities gtk-sharp3 python3 python3-pip

::::

::::{tab} macOS

First, install the `.NET SDK` package as per the installation instructions, which can be found on [the official .NET site](https://dotnet.microsoft.com/en-us/download/dotnet/8.0).
Make sure to install the right architecture, `Arm64` for Apple Silicon, `x64` for Intel

To install the remaining prerequisites, use:

    brew install binutils gnu-sed coreutils dialog cmake
    xcode-select --install

:::{note}
   This requires [homebrew](https://brew.sh/) to be installed in your system.
:::

::::


::::{tab} Windows

Building Renode on Windows uses MinGW and Git Bash, and requires you to properly set up the system environment.

**Git**

1. Download and install `git` using the default options
   You can get it from [the official website](https://git-scm.com/downloads).
2. Ensure the installation directory (`C:\Program Files\Git` by default) is in the system `PATH` variable. 

:::{note}
Prior to cloning the repository on *Windows*, git has to be configured appropriately. Run the following commands in Git Bash to set the options correctly:

    git config --global core.autocrlf false
    git config --global core.symlinks true
:::

**Python 3**

1. Download and install the Windows version of the Python 3 framework from [the Python website](https://www.python.org/downloads/).
2. Add location of the binaries to the system `PATH` variable. The installer can do this for you.

**MinGW**

:::{note}

The download link is from the `MinGW-W64-builds` project, linked from [the official MinGW-W64 website](https://www.mingw-w64.org/downloads/#mingw-w64-builds)

:::

1. Download `MinGW-w64 15.1.0` with the `x86_64` architecture, `win32` threads [the download site](https://github.com/niXman/mingw-builds-binaries/releases/download/15.1.0-rt_v12-rev0/x86_64-15.1.0-release-win32-seh-msvcrt-rt_v12-rev0.7z).
2. Extract the downloaded package and add its `mingw64\bin` directory (for example `C:\mingw-w64\mingw64\bin`) to the system `PATH` variable.

**CMake**

1. Download `CMake` and install Windows CMake from [the CMake website](https://cmake.org/download/).
2. Ensure that the installation directory is in the system `PATH`. The installer will offer to do this for you

**C# build tools**

See [the official .NET site](https://dotnet.microsoft.com/en-us/download/dotnet/8.0) for instructions on how to install `.NET SDK`.

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
On Windows, the building process described in this section can only be executed in Git Bash.
:::

To build Renode, run:

    ./build.sh

There are some optional flags you can use:

    -c                                clean instead of building
    -d                                build Debug configuration
    -v                                verbose output
    -p                                create packages after building
    -t                                create a portable package
    --source-package                  build a source package (dotnet on Linux only)
    -n                                tag built packages as nightly
    -s                                update submodules
    -b                                custom build properties file
    --skip-fetch                      skip fetching submodules and additional resources
    --no-gui                          build with GUI disabled
    -B                                bundle target runtime (default value: linux-x64, requires -t)
    -F                                select the target framework for which Renode should be built (default value: net8.0)
    --profile-build                   build optimized for profiling
    --tlib-coverage                   build tlib with coverage reporting
    --external-lib-only               only build external libraries
    --external-lib-arch               build only single arch (implies --external-lib-only)
    --tlib-export-compile-commands    build tlibs with 'compile_commands.json' (requires --external-lib-arch)
    --host-arch                       build with a specific tcg host architecture (default: i386)
    --skip-dotnet-target-generation   don't generate 'Directory.Build.targets' file, useful when experimenting with different build settings
    --tcg-opcode-backtrace            collect a backtrace for each emitted TCG opcode, to track internal TCG errors (implies Debug configuration)
    --shared                          build the librenode native library
    --ui                              rebuild the web-based UI


Additionally you can directly specify flags which will be passed to the build system after `--`.
For example, if you wanted to override the `CompilerPath` property you could use::

    ./build.sh -- p:CompilerPath=/path/to/gcc

You can also build `Renode.sln` from your IDE (like Visual Studio), but the `build.sh` script has to be run at least once.

## Creating packages

The build script can create native packages only, i.e., you must run it on Windows to create an `.exe` installer package, on Linux for `.deb`, `.rpm` and `.pkg.tar.xz` packages or on macOS for the `.dmg` image.

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

The packaging process described in this section can only be executed in Git Bash.

:::

1. Download and install [Inno Setup](https://jrsoftware.org/isdl.php) and add it to the Windows system `PATH` variable

::::

### Building

To build binary packages, run:

    ./build.sh -p

To build portable packages (embedding the dotnet runtime into the binary), run:

    ./build.sh -t

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

`renode/output/packages/RenodeSetup-<version>.exe`

:::
