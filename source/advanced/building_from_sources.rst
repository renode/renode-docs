.. _building-from-source:

Building Renode from source
===========================

This document provides detailed information on how to prepare the build environment, and then build and test Renode itself.

System requirements
-------------------

Linux
+++++

The following instructions have been tested on Ubuntu 16.04, however there should not be any major issues preventing you from using other (especially Debian-based) distributions as well.

Renode requires Mono >= 5.0 and several other packages.
To install them, use::

   sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
   echo "deb http://download.mono-project.com/repo/ubuntu xenial main" | sudo tee /etc/apt/sources.list.d/mono-xamarin.list
   sudo apt-get update
   sudo apt-get install git mono-complete automake autoconf libtool g++ realpath \
                        gksu libgtk2.0-dev screen uml-utilities gtk-sharp2 python2.7

.. note::

    Modify the distribution name (i.e., `ubuntu xenial` in the second command) according to your setup.

Mac
+++

Renode requires the Mono framework, which can be downloaded from `the official Mono project website <https://download.mono-project.com/archive/mdk-latest-stable.pkg>`_.

To install the remaining prerequisites of Renode, use::

   brew install binutils gnu-sed coreutils homebrew/versions/gcc49 dialog

.. note::

   This requires `homebrew <http://brew.sh/>`_ to be installed in your system.

Windows
+++++++

Building Renode on Windows is based on Cygwin and requires you to properely set up the system environment.

Gtk#
~~~~

1. Download and install *Gtk# 2.12.30* (this precise version is required) from `the Xamarin website <http://download.xamarin.com/GTKforWindows/Windows/gtk-sharp-2.12.30.msi>`_.

2. Add location of the binaries (``C:\Program Files (x86)\GtkSharp\2.12\bin`` by default) to the system ``PATH`` variable.

Cygwin
~~~~~~

1. Download `Cygwin installer <https://cygwin.com/setup-x86_64.exe>`_.

2. Install it with an additional module: ``openssh``.

3. You need to have ``git`` installed, either as a Cygwin package, or natively. If you use it as a native Windows application, you have to add the installation directory to the system ``PATH`` variable.

.. note::

    Prior to cloning the repository on *Windows*, git has to be configured appropriately:

    ``git config --global core.autocrlf false``

    ``git config --global core.symlinks true``

Python 2.7
~~~~~~~~~~

1. Download and install **native** Windows Python framework from `the Python website <https://www.python.org/downloads/>`_.

.. note::

   Do not use the module provided by ``Cygwin``. If you have Cygwin's version of Python already installed, make sure that the native's version location is included at the beginning of Cygwin's PATH variable.

2. Add location of the binaries (``C:\Python27`` by default) to the system ``PATH`` variable.

C build tools
~~~~~~~~~~~~~

1. Download the `MinGW installer <https://sourceforge.net/projects/mingw/files/Installer/mingw-get-setup.exe>`_.

2. Install it with the ``mingw32-base`` and ``mingw32-pthreads-w32`` modules.

3. Add location of the binaries (``C:\MinGW\bin`` by default) to the system ``PATH`` variable.

C# build tools
~~~~~~~~~~~~~~

1. Download `VS Build Tools 2017 <https://www.visualstudio.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15#>`_.

2. Run the installer, select *Visual Studio Build Tools 2017* product and click *Install* or *Modify*.

3. Switch to the *Individual components* pane and select:

    * *.NET Framework 4 targeting pack* and *.NET Framework 4.5 targeting pack* in section *.NET*,

    * *NuGet targets and build tasks* in section *Code tools*.

4. Add location of the binaries (``C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\MSBuild\15.0\Bin\amd64`` by default) to the system ``PATH`` variable.

Installing python modules
-------------------------

Install additional modules required for Robot Framework integration::

    python -m pip install robotframework netifaces requests psutil

Downloading the source code
---------------------------

Renode’s source code is available on GitHub::

   git clone https://github.com/renode/renode.git

Submodules will be automatically initialised and downloaded during the build process, so you do not need to do it at this point.

Building Renode
---------------

.. note::

    On Windows, the building process described in this section can only be executed in Cygwin shell.

To build Renode, run::

   ./build.sh

There are some optional flags you can use::

   -c          clean instead of building
   -d          build in debug configuration
   -v          verbose mode
   -p          build binary packages (requires some additional dependencies)

You can also build ``Renode.sln`` from your IDE (like MonoDevelop or Visual Studio), but the ``build.sh`` script has to be run at least once.

Creating packages
+++++++++++++++++

The build script can create native packages only, i.e., you must run it on Windows to create a zip archive, on linux for deb, rpm and tar.xz packages or on OSX for the dmg image.

After completing successfully, the script will print the location of the files created.
