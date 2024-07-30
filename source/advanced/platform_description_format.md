# Platform description format

To address the need of easily assembling peripheral models into complete platform definitions, a YAML-like platform description format was created for Renode based on common use cases as experienced in daily work with the framework.

Typically, files in this format have the `.repl` (REnode PLatform) extension.

The format is meant to be human-readable, concise, easy to parse, base upon, extend and modify.

## Indentation

Within Renode's platform description format, meaningful indentation (similar to e.g. Python) is used *alongside* curly braces (`{`, `}`).
The rules are as follows:

1. Only spaces are used for indentation and indent has to be a multiple of four spaces.
2. Syntactically one level of indentation corresponds to one brace (opening one if we indent, and closing if dedent).
3. The indentation inside braces is not meaningful, this also applies to new line characters.
   They are all treated as white characters.
   When meaningful indentation is used, we refer to it as indent mode (as opposed to non-indent mode).
   To separate elements in non-indent mode (corresponding to lines in indent mode), a semicolon must be used.

For example these files are equivalent:

``` none
line1
line2
    line3
    line4
        line5
    line6
```

``` none
line1
line2 { line3; line4 { line5 }; line 6 }
```

## Comments

There are two types of comments:

- line comments start with `//` and continue to the end of the line;
- multiline comments are delimited by `/*` and `*/` and can span multiple lines.

Both comments can be used in indent and non-indent mode, but there is one special rule.
When a multiline comment spans multiple lines, it has to end at the end of the line.
Otherwise it would be difficult to establish what indenation should be used for the rest of the line.

In other words this source is legal:

``` none
line1 /* here a comment starts
 here it continues
and here ends*/
line2
```

But this one is not:

``` none
line1 /* here a comment starts
 here it continues
and here ends*/ line2
```

## Basic structure

Each platform description format consists of *entries*.
An entry is a fundamental unit of peripheral description.
The basic format of an entry is as follows:

``` none
variableName: TypeName registrationInfo
    attribute1
    attribute2
    ...
    attributeN
```

All of `TypeName`, `registrationInfo` and `attributes` are optional, but at least one of them must be present.
If an entry contains a TypeName, then it is a *creating entry* (otherwise it is an *updating entry*).

Each creating entry declares a variable, there can be only one declaration for a given variable and it must be the first entry that is encountered when parsing the file, unless the variable is declared before parsing.
For example all peripherals that are registered in the machine are also imported as variables and can have their updating entries (but not creating entries).

In other words this code is legal:

``` none
variable1: SomeType
    property: value

variable1:
    property: otherValue
```

But the following results in an error:

``` none
variable1:
    property: value

variable1: SomeType
    property: otherValue
```

The consecutive entries (for the given variable) are called updating because they can update some information provided by the former ones.
Eventually all entries corresponding to the given variable are *merged* so that the merge result contains attributes from all entries, possibly some invalidated by some other.

TypeName must be provided with the full namespace the type is located in.
However, if the namespace starts with `Antmicro.Renode.Peripherals`, then this part can be omitted.

A creating entry can have an optional prefix `local`, then the variable declared in this entry is called a *local* variable.
The prefix is only used with a creating entry, not with an updating one.

For example:

``` none
local cpu: SomeCPU
    StringProp: "a"

cpu:
    IntProp: 32
```

If the variable is local, then we can reference it only within that file.
This will be clearer after reading the next section, but generally if one file depends on another, both can declare same named local variable and they are completely independent, in particular they can have different types.

## Depending on other files

One description can depend on another, in which case it can use all (non-local) variables from that file.
Note that also all non-local variables from a file we\'re depending on cannot have creating entries.
In other words, depending on another file is like having it pasted at the top of the file with the exception of local variables.

The `using` keyword is used to declare a dependency:

``` none
using "path"
```

The line above is called a *using entry*.
All using entries have to come before any other entries.
There is also a syntax that lets the user depend on a file but prepend all variables within that file with a prefix:

``` none
using "path" prefixed "prefix"
```

Then `prefix` is applied to each variable in `path`.

Since files mentioned in `path` can further depend on other files, this can sometimes lead to a cycle.
This is detected by the format interpreter and an error with information about the cycle is generated.

## Values

A *value* is a notion widely used in the platform description format.
There are three kinds of values:

- *simple values* that can be further divided into:
  - strings (delimited by a double quote with `\"` used as an escaped double quote);
  - multiline strings (delimited by triple quotes `'''` with `\'''` used as escaped triple quotes) (example below);
  - boolean values (either `true` or `false`);
  - numbers (decimal or hexadecimal with the `0x` prefix);
  - ranges (described below)
- reference values, which point to a variable and are given just as the name of the variable;
- inline objects that denote an object described in the value itself and not tied to any variable (described later).

A range represents an interval and can be supplied in two forms:

- `<begin, end>` or
- `<begin, +size>` where `begin`, `end` and `size` are decimal or hexadecimal numbers.

Examples: `<0, 100>`, `<0x10000, +0x200>`.

Example of a multline string with an escaped delimiter:

``` none
name: '''this is \'''
some 
multiline
name'''
```

## Registration info

Registration info tells in which register a given peripheral should be registered and how.
A peripheral can be registered in one or more registers.
For a single registration the format of registration info is as follows:

``` none
@ register registrationPoint as "alias"
```

where `registrationPoint` is a value and is optional.
The `as "alias"` part is called an *alias* and is also optional.
Using `registrationPoint`, the registration point is created or directly used (if the value specified is a registration point):
If the registration point is not given, then either a `NullRegistrationPoint` is used or (if `NullRegistrationPoint` is not accepted) a registration point with no constructor parameters or all parameters optional.

If the registration point is a simple value, then a registration point is used with a constructor taking one parameter to which this simple value can be converted and possibly other optional parameters.
Note that any ambiguity in the two cases mentioned above will lead to an error.

If the registration point is a reference value or an inline object then they are directly used as a registration point.

During registration, the registered peripheral is normally given the same name as the name of the variable.
The user can, however, override this name with a different one using the mentioned alias.

Multiple registrations are also supported; this has the following form:

``` none
@ {
    register1 registrationPoint1;
    register2 registrationPoint2;
    ...
    registerN registrationPointN
} as "alias"
```

The meaning and optionality of the elements is the same as it was in the previous case with the only difference that the peripheral is registered multiple times, possibly in different registers.
Note that - as was mentioned at the beginning of this document - the indentation within braces does not matter.

Registration info can be given in any entry (creating or updating), also in more than one entry.
In such case only the registration from the newest entry takes place.
Registration can also be cancelled, i.e. overridden without providing new registration info.
This is done using `@ none` notation, for example:

``` none
variable: @none
```

## Attributes

There are three kinds of attributes:

-   constructor or property attributes;
-   interrupt attributes;
-   init attributes.

### Constructor or property attributes

A constructor or property attribute has the following form:

``` none
name: value
```

`name` is the name of the property (if the initial letter is uppercase) or constructor parameter (otherwise) and `value` is a value.
When used with a property, if the attribute\'s value is convertible to this property type, then such converted value will be set (otherwise an error is produced).

Note, however, that another entry may update the property so that only the final (i.e. the last containing an attribute setting this property) entry is effective.

The `none` keyword can also be used instead of a value.
Having it there means that the property is not set using any value and its value *before applying the description* is kept.
It can be useful when some entry sets some value and we want to update this entry but not set any value.

The `empty` keyword can be used to set the default value of property or constructor parameter:

- numerical values are set to `0`;
- string values are set to `null`;
- enum values are set to value corresponding to `index 0` in this enum;
- reference types are set to `null`;

Constructor attributes are merged in a similar way, i.e. attributes from all entries belonging to the given variable are analyzed and for each name we take the last one value with this name.
The constructor of the peripheral is chosen based on the set of merged attributes.
For each possible constructor of the type specified in the creating entry we check whether:

-   each parameter of the constructor has a default value or corresponding attribute, i.e. attribute having same name as the name of the parameter;
-   the corresponding attribute has value convertible (for simple types) or assignable (otherwise) to the parameter type;
-   all attributes have been used.

If all the conditions are satisfied then the analyzed constructor is marked as usable.
If only one constructor is usable, then the object is created using this constructor.
If there is no such constructor or there are more than one, an error is produced.

Because it is much easier to debug constructor selection problems if all the data are in one place (i.e. name of the type and constructor attributes), a warning is issued whenever a non creating entry contains constructor parameters (effectively updating a creating one).

Note that it is only possible to provide constructor attributes for an entry whose variable is going to be created, so it is not possible to provide any on variables represeting peripherals existing before a given description is processed.

### Interrupt attributes

As the name suggests, interrupt attributes are used to specify which interrupts of the variable in which the attribute is defined are connected and where.
The simplest format of such attribute is as follows:

``` none
-> destination@number
```

where `destination` is a variable implementing the `IGPIOReceiver` interface and `number` is the destination interrupt number.
Note that there is nothing specified on the left side - this is only possible if there is a single property of type `GPIO`, or there are multiple properties, but one of them is marked with a `DefaultInterrupt` attribute. This is the one that gets connected.

Whenever the user wants to specify which property should be connected, a more general form can be used:

``` none
propertyName -> destination@number
```

where `propertyName` is the name of the property (of the `GPIO` type) that should be connected.
Also, if the type implements `INumberedGPIOOutput`, a number can be used instead of the property name.

If more than one interrupt is to be connected to the same destination peripheral, the following form of the attribute can be used:

``` none
[irq1, irq2, ..., irqN] -> destination@[irqDest1, irqDest2, ..., irqDestN]
```

Where `irq1` connects to `irqDest1` etc.
Again, `irq` s can be names or numbers (if `INumberedGPIOOutput` is implemented) and `irqDest` s have to be numbers.
Naturally, the arity of sources and destinations has to match.

There is also a possibility of connecting a single source to multiple destinations with the `|` sign, which can be used with every interrupt attribute format:

``` none
-> destination@number | another_destination@number
propertyName -> destination@number | another_destination@number
[irq1, irq2, ..., irqN] -> destination@[irqDest1, irqDest2, ..., irqDestN] | another_destination@[irqDest1, irqDest2, ..., irqDestN]
```

Note that every attribute separated by the `|` sign has to be of the same arity as the source.

There is also a notation used in case of local interrupts:

``` none
source -> destination#index@interrupt
```

`destination` has to implement `ILocalGPIOReceiver` and `index` is the index of the local GPIO receiver.
This notation can also be used with multiple interupts:

``` none
[irq1, irq2, ..., irqN] -> destination#index@[irqDest1, irqDest2, ..., irqDestN]
```

Just as in the case of properties, interrupt attributes can update older ones.
This is done basing on the source interrupt, i.e. if two attributes from different entries use the same source interrupt, only the one from the latter is used.
Again, as in properties, the user may want to cancel the irq connection without specifying a different one.
The keyword `none` can be used for this purpose:

``` none
source -> none
```

### Init attributes

Init attributes are used to execute monitor commands on the variable.
They have one of the following forms:

``` none
init:
    monitorStatement1
    monitorStatement2
    ...
    monitorStatementN
```

``` none
init add:
    monitorStatement1
    monitorStatement2
    ...
    monitorStatementN
```

The difference between them is that during merge phase the first one overrides the given variable\'s previous init attribute (if there is one) and the second one concanates itself to that previous one.
The final entry is eventually executed: every statement is prepended with the name of the peripheral the variable is tied to and then directly parsed by the Monitor.
Note that this means that the init section is only legal for variables that are registered.

## Inline objects

Inline objects are values similar to reference values, but instead of creating a separate variable and then referencing it, it is defined directly in the place of reference.
The form is as follows:

``` none
new Type
    attribute1
    attribute2
    ...
    attributeN
```

The effect is the same as creating an entry of this type and with those attributes, but it cannot be updated and is only available in the place of reference.
So, for example, these codes lead to the same effect:

``` none
variable: SomeType
    SomeProperty: point

point: Point
    x: 5
    y: 3
```

``` none
variable: SomeType
    SomeProperty: new Point {x: 5; y: 3}
```
