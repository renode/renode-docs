# Sensors and virtual environment

Renode enables you to manipulate virtual environmental conditions like `Temperature` and `Humidity` for sensors in the emulation.
Sensors can be either controlled individually by directly setting their values (in the simple use case) or globally using an `Environment` medium (in order to implement scenarios with multiple sensors reading consistent virtual environmental conditions).

## Controlling individual sensors

To control an individual sensor in your Renode machine, you need to access the appropriate property available to the sensor.
To change the `Temperature` property of a sensor, use:

```
(machine-0) spi0.temperatureSensor Temperature 36.6
```

This value can then be read by accessing the same property::

```
(machine-0) spi0.temperatureSensor Temperature
36.6
```
    
## Controlling sensors globally

For more advanced use cases, Renode offers the `Environment` object, which is an abstract medium representing a space with physical properties.
It allows you to group and manage sensors that should observe the same environmental conditions.

### Creating an environment

To create an environment called `env`, execute:

```
(monitor) emulation CreateEnvironment "env"
```

You can create multiple environments as needed.
Currently, `Environment` supports two parameters: temperature and pressure.

You can set the temperature in the environment by calling:

```
(monitor) env Temperature 36.6
```

To check the current setting:

```
(monitor) env Temperature
36.6
```

### Adding sensors to an environment

There are two ways of adding sensors to an environment:

* add a single sensor from a machine,
* add a machine to an environment.

You have to be in a {ref}`machine context <machine-context>` to be able to execute the following commands.

#### Adding a single sensor

To add the `temperatureSensor` peripheral, connected via the `i2c` bus, run:

```
(machine-0) i2c.temperatureSensor SetEnvironment env
```

Only the specified sensor will be added to the `env` environment and will observe the temperature value of that environment.

#### Adding a machine

To add the current machine to the environment, run:

```
(machine-0) machine SetEnvironment env
```

This command will connect the machine and all of its sensors to the environment `env`.
They will have the same temperature value as the environment.

```{note}
When connecting a machine to an environment, all its sensors that were previously connected to other environments will be reconnected as well.
```

Sensors added to an environment will be updated every time the environment changes.
However, you can still set your own value on a specific sensor, and it will not be propagated to other sensors (until a change in the environment overrides this).
