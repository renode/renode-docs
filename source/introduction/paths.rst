Paths
=====

Passing paths to files
----------------------

As described in :ref:`the monitor section <monitor>` in most cases paths in Monitor
starts with the special ``@`` sign.

Path configuration
------------------

When interpreting a path, Renode looks in several places based on the configured internal ``path``.
By default:

* it first checks in the Renode root directory,
* if the file was not found in the root directory, it checks the current working directory.

You can check and modify the path configuration using the ``path`` command in Monitor.

Type ``help path`` in Monitor to see details::

    (monitor) help path
    path
    allows modification of internal 'PATH' variable.

    Current 'PATH' value is: /home/antmicro/renode;/home/antmicro
    Default 'PATH' value is: /home/antmicro/renode

    You can use following commands:
    'path set @path'        to set 'PATH' to the given value
    'path add @path'        to append the given value to 'PATH'
    'path reset'            to reset 'PATH' to it's default value


Relative paths
--------------

If you want to express path that is relative to the currently executed Renode script (.resc) you can use the ``$ORIGIN`` variable::

    include $ORIGIN/my_subscript.resc

An example of usage can be found in `the fomu script <https://github.com/renode/renode/blob/8ae7fdfc6cbe7b01952a8b2d4517d14aff7a297e/scripts/complex/fomu/renode_etherbone_fomu.resc#L5>`_.

.. note::

    There is no ``@`` at the beginning of the ``$ORIGIN``-based path.

.. note::

    The ``$ORIGIN`` variable is only available inside a script - it won't work interactively in Monitor.

In Monitor you can use a special ``$CWD`` variable to provide path that is relative to the current working directory::

    (machine-0) include $CWD/my_script.resc

.. note::

    There is no ``@`` at the beginning of the ``$CWD``-based path.

Paths in Robot files
--------------------

In the Robot file you can also use another variable: ``${CURDIR}``.

.. note::

    ``${CURDIR}`` is handled and resolved on the Robot Framework level and has nothing to do with Renode.

Paths starting with ``${CURDIR}`` are relative to the Robot file location.

An example of usage can be found in `the LSM9DS1 test <https://github.com/renode/renode/blob/8ae7fdfc6cbe7b01952a8b2d4517d14aff7a297e/tests/peripherals/LSM9DS1.robot#L24>`_.

.. note::
    A ``${CURDIR}``-based path needs to be prepended with ``@``.
    Since it is resolved at the Robot Framework level, for Renode it looks like a any other path provided by a user.

