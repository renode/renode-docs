Renode documentation
====================

This repository contains documentation of the `Renode Framework <https://www.renode.io>`_, a virtual development tool for multinode embedded networks by Antmicro.

The documentation is hosted at `Read the Docs <https://renode.readthedocs.org>`_.

Building procedure
------------------

To build the documentation as HTML run::

    make html

To build a PDF file run::

   make latexpdf

Requirements for Linux
----------------------

* Sphinx 1.5
* myst-parser, sphinx_tabs, sphinxcontrib-svg2pdfconverter modules
* texlive-full (for the PDF version)
