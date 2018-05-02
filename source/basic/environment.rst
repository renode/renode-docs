Environment
===========

In Renode, an Environment is an abstract medium that represents a space with physical properties.
It allows you to group and manage sensors that should observe the same environmental conditions.

Creating an environment
-----------------------

To create an environment called ``env``, execute::

    (monitor) emulation CreateEnvironment "env"

You can create multiple environments as needed.
Currently, environments support two parameters: temperature and pressure.

You can set the temperature in the environment, by calling::

    (monitor) env Temperature 36.6

To check the current setting::

    (monitor) env Temperature
    36.6

Adding sensors to an environment
--------------------------------

There are two ways of adding sensors to an environment:

* add a single sensor from a machine,
* add a machine to an environment.

You have to be in a :ref:`machine context <machine-context>` to be able to execute the following commands.

Add a single sensor
+++++++++++++++++++

To add the ``temperatureSensor`` peripheral, connected via the ``i2c`` bus, run::

    (machine-0) sysbus.i2c.temperatureSensor SetEnvironment env

Only the specified sensor will be added to the ``env`` environment and will observe the temperature value of that environment.

Add a machine
+++++++++++++

To add the current machine to the environment, run::

    (machine-0) machine SetEnvironment env

This command will connect the machine and all of its sensors to the environment ``env``.
They will have the same temperature value as the environment.

.. note::

    When connecting a machine to an environment, all its sensors that were previously connected to other environments will be reconnected as well.

Sensors added to an environment will be updated every time the environment changes, however you can still set your own value on a specific sensor, and it will not be propagated to other sensors (until a change in the environment overrides this).

Accessing the readings of a sensor
----------------------------------

To check the reading of a sensor, execute::

    (machine-0) sysbus.i2c.temperatureSensor Temperature
    36.60

To change the reading of a sensor, execute::

    (machine-0) sysbus.i2c.temperatureSensor Temperature 37
