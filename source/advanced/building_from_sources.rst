.. _building-from-source:

Building Renode from source
===========================

This document provides detailed information on how to prepare the build environment, and then build and test Renode itself.

Prerequisites
-------------

Core prerequisites
++++++++++++++++++

.. tabs::

   .. group-tab:: Linux

      The following instructions have been tested on Ubuntu 16.04, however there should not be any major issues preventing you from using other (especially Debian-based) distributions as well.

      First, install the ``mono-complete`` package as per the installation instructions for various Linux distributions which can be found on `the Mono project website <https://www.mono-project.com/download/stable/#download-lin>`_.

      To install the remaining dependencies, use::

         sudo apt-get update
         sudo apt-get install git automake autoconf libtool g++ realpath policykit-1 \
                      libgtk2.0-dev screen uml-utilities gtk-sharp2 python2.7

   .. group-tab:: macOS

      On macOS, the Mono package can be obtained by using `a download link on the Mono project website <https://download.mono-project.com/archive/mdk-latest-stable.pkg>`_.

      To install the remaining prerequisites, use::

         brew install binutils gnu-sed coreutils dialog
         xcode-select --install

      .. note::

         This requires `homebrew <https://brew.sh/>`_ to be installed in your system.

   .. group-tab:: Windows

      Building Renode on Windows is based on Cygwin and requires you to properly set up the system environment.

      .. rubric:: Cygwin

      1. Download `Cygwin installer <https://cygwin.com/setup-x86_64.exe>`_.
      2. Install it with an additional module: ``openssh``.

      .. rubric:: Git

      1. Download and install ``git`` as a **native** application.
         You can get it from `the official website <https://git-scm.com/downloads>`_.
         You can use either a regular installation or a portable version.
      2. Ensure the installation directory (``C:\Program Files\Git`` by default) is in the system ``PATH`` variable.
         The installer offers to install a subset of ``git`` tools in ``PATH``, this is the recommended option.

      .. note::

          Prior to cloning the repository on *Windows*, git has to be configured appropriately::

              git config --global core.autocrlf false
              git config --global core.symlinks true

      .. rubric:: Python 2.7

      1. Download and install **native** Windows Python framework from `the Python website <https://www.python.org/downloads/>`_.

      .. note::

         Do not use the module provided by ``Cygwin``.
         If you have Cygwin's version of Python already installed, make sure that the native's version location is included at the beginning of Cygwin's PATH variable.

      2. Add location of the binaries (``C:\Python27`` by default) to the system ``PATH`` variable.

      .. rubric:: C build tools

      1. Download the `MinGW-w64 installer <https://netix.dl.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/mingw-w64-install.exe>`_.
      2. Install the latest version with the ``x86_64`` architecture, ``win32`` threads and ``sjlj`` exception handling.
      3. Add the location of the binaries (it depends on the MinGW version and installation settings e.g. ``C:\Program Files\mingw-w64\x86_64-8.1.0-win32-sjlj-rt_v6-rev0\mingw64\bin``) to the system ``PATH`` variable.

      .. rubric:: C# build tools

      1. Download `VS Build Tools 2017 <https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15>`_.
      2. Run the installer, select the *Visual Studio Build Tools 2017* product and click *Install* or *Modify*.
      3. Switch to the *Individual components* pane and select:

         * *.NET Framework 4.5 targeting pack* in section *.NET*,
         * *NuGet targets and build tasks* in section *Code tools*.

      4. Add the location of the binaries (``C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\MSBuild\15.0\Bin\amd64`` by default) to the system ``PATH`` variable.

Downloading the source code
---------------------------

Renode’s source code is available on GitHub::

   git clone https://github.com/renode/renode.git

Submodules will be automatically initialised and downloaded during the build process, so you do not need to do it at this point.

Additional prerequisites (for Robot framework testing)
++++++++++++++++++++++++++++++++++++++++++++++++++++++

If you followed the instructions above, Python should be installed in your system.
Install the ``pip`` package manager and some additional modules to enable writing and running test cases with the Robot framework::

    python -m pip install -r tools/requirements.txt

Building Renode
---------------

.. note::

    On Windows, the building process described in this section can only be executed in a Cygwin shell.

To build Renode, run::

   ./build.sh

There are some optional flags you can use::

   -c          clean instead of building
   -d          build in debug configuration
   -v          verbose mode
   -p          build binary packages (requires some additional dependencies)

You can also build ``Renode.sln`` from your IDE (like MonoDevelop or Visual Studio), but the ``build.sh`` script has to be run at least once.

Creating packages
-----------------

The build script can create native packages only, i.e., you must run it on Windows to create an ``.msi`` installer package, on Linux for ``.deb``, ``.rpm`` and ``.pkg.tar.xz`` packages or on macOS for the ``.dmg`` image.

There is also a separate procedure to create `Conda <https://docs.conda.io/en/latest/>`_ packages, described in a `dedicated README <https://github.com/renode/renode/tree/master/tools/packaging/conda>`_.

Prerequisites
+++++++++++++

Depending on the system, there may be some prerequisites for building Renode packages.

.. tabs::

    .. group-tab:: Linux

        Run::

            sudo apt-get install ruby ruby-dev rpm bsdtar
            sudo gem install fpm

    .. group-tab:: macOS

        No additional prerequisites for macOS.

    .. group-tab:: Windows

        .. note::

            On Windows 10, it is important to enable .NET 3.5 in the system before installing the WiX Toolset.

            The packaging process described in this section can only be executed in a Cygwin shell.

        1. Download and install the `WiX Toolset installer <https://wixtoolset.org/releases/>`_ (version at least 3.11).
        2. Add the ``zip`` package to Cygwin.

Building
++++++++

To build binary packages, run::

    ./build.sh -p

The packages will have a version assigned to them, defined by the contents of the ``tools/version`` file.

You can also build nightly packages with::

    ./build.sh -pn

This will append a date and a commit SHA to the output files.

Location of packages
++++++++++++++++++++

After completing successfully, the script will print the location of the files created:

.. tabs::

    .. group-tab:: Linux

       ``renode/output/packages/renode_<version>.{deb|rpm|tar.gz}``

    .. group-tab:: macOS

       ``renode/output/packages/renode_<version>.dmg``

    .. group-tab:: Windows

       ``renode/output/packages/renode_<version>.msi``
