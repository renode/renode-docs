# Renode Sensor Data Format (RESD)

For an introduction and description of simple operations on your simulated sensors, such as assigning a constant value as a sensor readout, see the {doc}`../basic/sensors` chapter.

## What is the Renode Sensor Data format?

Renode Sensor Data (RESD) is a unified and portable way to provide sample data for sensor models implemented in Renode.
Sensor data described in `.resd` files use standard units and fixed formats for all data types, so they can be used by any existing or future model.

The data stored in a `.resd` file is divided into independent channels, each of a given type (e.g. temperature or acceleration).
This allows a single input file to be used for multiple sensors such as IMU.
It is also possible to include multiple channels of the same type (each identified by a unique channel ID), e.g. two channels for temperature readings.

Each `.resd` file consists of a single file header followed by a variable number of data blocks:

```
00000000  52 45 53 44 01 00 00 00  02 01 00 00 00 a8 01 00  |RESD............|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 70 c9  |..............p.|
00000020  b2 8b 00 00 00 00 00 00  00 00 00 00 00 cc 9b 03  |................|
00000030  00 c4 95 03 00 79 9b 03  00 18 9a 03 00 75 a3 03  |.....y.......u..|
00000040  00 3b a1 03 00 b1 b4 03  00 8d 9d 03 00 41 a5 03  |.;...........A..|
00000050  00 4d 9b 03 00 21 af 03  00 6f 96 03 00 20 ba 03  |.M...!...o... ..|
```

You can easily create a binary file like the one shown above from a CSV file using the [CSV - RESD parser](csv-resd).

The file header consists of a 4-byte magic string value `RESD` encoded in ASCII, followed by a single byte defining the version of the format the file uses (the code above uses version 0x1), followed by 3 bytes of reserved padding (currently defined as all zeros).

## RESD Data Blocks

Each block header is structured in the following way:

```{csv-table} Block header structure
:header-rows: 1
:delim: "|"

Bytes | 0          | 1 - 2       | 3 - 4      | 5 - 8
Name  | Block type | Sample type | Channel id | Data size
```

### RESD Block Types

Currently, you can use the following block types in your `.resd` files:

```{csv-table} Block types
:header-rows: 1
:delim: "|"

ID  | Block type
0x0 | Reserved
0x1 | [Arbitrary Timestamp Sample Blocks](arbitrary-timestamp-sample-blocks)
0x2 | [Constant Frequency Sample Blocks](constant-frequency-sample-blocks)
```

(arbitrary-timestamp-sample-blocks)=

#### Arbitrary timestamp sample blocks

Arbitrary timestamp sample blocks contain a series of samples, each with its own [timestamp](timestamps).
In this type of sample block, you do not specify a period between samples, but instead provide a specific timestamp for each sample to simulate irregular sensor readings.

(constant-frequency-sample-blocks)=

#### Constant frequency sample blocks

In constant-frequency blocks, the block header is 16 bytes longer than the arbitrary timestamp block and includes an additional sub-header that provides information about the timestamp of the first sample in a series and a period between consecutive samples.

```{note}
If your block contains more than 1 sample, the period value of `0` is invalid.
```

(timestamps)=

#### Timestamps

Timestamps in `.resd` are encoded as unsigned 8-byte values expressed in virtual nanoseconds counted from the beginning of the file.

```{note}
The `.resd` parser can optionally support a global timestamp addend applied to all samples in the file (e.g. to allow loading the same input file twice at different moments in virtual time).
```

### RESD Sample Types

Your `.resd` files can contain the following sample types:

```{csv-table} Sample types
:header-rows: 1
:delim: "|"

ID              | Sample Type  | Sample Unit
0x0000          | Reserved     | N/A
0x0001          | Temperature  | signed 4-byte value in millidegrees (10^-3) Celsius
0x0002          | Acceleration | set of 3 signed 4-byte values in micro g (10^-6)<br> mapped to X, Y, Z dimensions
0x0003          | Angular rate | set of 3 signed 4-byte values in tens of microradians<br> (10^-5)  per second mapped to X, Y, Z dimensions
0x0004          | Voltage      | unsigned 4-byte value in microvolts (10^-6) 
0x0005          | ECG          | signed 4-byte value in nanovolts (10^-9) 
0xF000 - 0xFFFF | Custom       | defined by model-specific input
```

Keep in mind that sample types other than Custom do not utilize a [metadata](metadata) dictionary (metadata size set to 0).

```{note}
Using a custom sensor data type makes the input data tightly coupled to the particular sensor implementation, and therefore, it might not be compatible with other sensors.
```

(metadata)=

#### Metadata

Metadata is a binary-encoded dictionary, where each entry consists of a key name, key type, and value.
The first 8 bytes indicate the size of the metadata section and can be set to 0 to indicate that the given block contains no additional metadata.

The key name is a null-terminated string consisting of [a-z0-9_] characters.
It's followed by a byte that describes the type of the value for the given key:

```{csv-table} Metadata Types
:header-rows: 1
:delim: "|"

ID   | Metadata type
0x00 | Reserved
0x01 | int8
0x02 | uint8
0x03 | int16
0x04 | uint16
0x05 | int32
0x06 | uint32
0x07 | int64
0x08 | uint64
0x09 | float
0x0A | double
0x0B | string (null-terminated)
0x0C | blob
```

```{note}
In blob type metadata, the first 4 bytes encode the blob content length reset as an unsigned integer.
```

For example, the encoding of a metadata section consisting of two entries: a description of type string and data of type blob would look like this:

```{csv-table} Example metadata string and blob
:header-rows: 1
:delim: "|"

Bytes   | Name             | Value 
0 - 7   | Size             | 78
8 - 19  | Key #1 (string)  | Description\0
20      | Type #1 (string) | 0x0B
21 - 59 | Value #1         | This is a very important sample stream\0
60 - 64 | Key #3 (string)  | Data\0
65      | Type #3 (blob)   | 0x0C
66 - 69 | Blob size        | 0x5
70 - 74 | Blob content     | 0xDE 0xAD 0xC0 0xFF 0xEE
```

### Custom Sample Data Example - MAX86171 AFE

The following instructions show how to use RESD to create a custom sample data example based on a real sensor - [MAX86171 AFE](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX86171.pdf).

The measurements taken by the MAX86171 AFE sensor depend on the channel configuration, e.g. the LED exposure drive current value directly affects the photodiode output.
Therefore, each MAX86171 AFE sample data block begins with a metadata section containing a dictionary of the following information:

```{csv-table} Metadata string and blob example
:header-rows: 1
:delim: "|"

Key name          | Type   | Description
led_a_exposure    | uint16 | LED A exposure drive current in mA
led_a_source      | uint8  | LED A source
led_b_exposure    | uint16 | LED B exposure drive current in mA
led_b_source      | uint8  | LED B source
led_c_exposure    | uint16 | LED C exposure drive current in mA
led_c_source      | uint8  | LED C source
pd_a_source_flags | uint8  | PD A source/flags
pd_a_adc_range    | uint32 | PD A ADC range
pd_a_dac_offset   | int16  | PD A DAC offset
pd_b_source_flags | uint8  | PD B source/flags
pd_b_adc_range    | uint32 | PD B ADC range
pd_b_dac_offset   | int16  | PD B DAC offset
```

#### MAX86171 AFE Sample Data

A single MAX86171 AFE sample is described as a one-byte unsigned value containing a number of active channels followed by a list of measurement frames, each encoded as a four-byte unsigned value:

```{csv-table} MAX86171 AFE sample data structure
:header-rows: 1
:delim: "|"

Bytes            | 0                | 1 - 4    | 5 - 8    | (8N + 1) - (8N + 4)
Values [raw AFE] | Number of frames | Frame #0 | Frame #1 | Frame #N
```

An AFE sample in RESD corresponds to a single frame generated by the MAX86171 AFE: two tagged samples are required for each active measurement, as described in the FIFO Description section of the MAX86171 data sheet:

```{csv-table} MAX86171 AFE sample details
:header-rows: 1
:delim: "|"

Bits   | 31..24   | 23..20 | 19..0
Values | Reserved | Tag    | Value
```

The tag section follows the specification from the FIFO Description section of the sensor's data sheet:

```{csv-table} MAX86171 AFE sample details
:header-rows: 1
:delim: "|"

Tag  | Description
0x00 | Reserved
0x01 | Measurement 1 Data
0x02 | Measurement 2 Data
0x03 | Measurement 3 Data
0x04 | Measurement 4 Data
0x05 | Measurement 5 Data
0x06 | Measurement 6 Data
0x07 | Measurement 7 Data
0x08 | Measurement 8 Data
0x09 | Measurement 9 Data
0x0A | Dark Data
0x0B | ALC Overflow Event
0x0C | Exposure Overflow Event
0x0D | Picket Fence Event
0x0E | Invalid Data
0x0F | Reserved
```

A sample with data two measurement OC channel 1 would then look like this:

```{csv-table} MAX86171 AFE sample details
:header-rows: 1
:delim: "|"

Bytes  | 0          | 1 - 4                   | 5 - 8
Names  | No. frames | Frame 1 (Measurement 1) | Frame 2 (Measurement 1)
Values | 0x2        | 0x00 0x01 0x12 0x34     | 0x00 0x01 0x12 0x34
```

The frames can be decoded as:

```{csv-table} MAX86171 AFE decoded frames
:header-rows: 1
:delim: "|"

Bits   | 31..24   | 23..20            | 19..0
Names  | Reserved | Measurement 1 tag | Measurement value
Values | 0x000    | 0x1               | 0x1234
```

(csv-resd)=

### CSV - RESD parser usage

The [CSV - RESD parser](https://github.com/renode/renode/tree/master/tools/csv2resd) is a tool in the Renode repository that allows you to convert CSV files to the RESD file format.

To use the tool, follow this syntax:

```
./csv2resd.py [GROUP]
GROUP ::= -i <csv-file> [-m <type>:<field(s)>:<target(s)>*:<channel>*]
          -s <start-time> -f <frequency> -t <timestamp> -o <offset> -c <count>
```

The syntax allows multiple group specifications, where --input is a separator between groups.
You can specify multiple mappings (`-map`) for each `--input`.

The `*` in `--map` indicates that the given property is optional.
For your `--map` argument to be correct, it must be structured in one of the following ways:

* `--map <type>:<field(s)>`
* `--map <type>:<field(s)>:<target(s)>`
* `--map <type>:<field(s)>:<target(s)>:<channel>`
* `--map <type>:<field>::<channel>`

See `--help` for more information.

If you wanted to extract the columns `temp1` and `temp2` from the file `first.csv` and first 3 samples `temp` from the file `second.csv` and then map them to the temperature channels `0`, `1` and `2` in RESD, respectively, you would run the script with the following parameters:

```
./csv2resd.py \
    -i first.csv \
        -m temperature:temp1::0 \
        -m temperature:temp2::1 \
        -s 0 \
        -f 1 \
    -i second.csv \
        -m temperature:temp::2 \
        -s 0 \
        -f 1 \
        -c 3 \
    output.resd
```

### RESD introspection

Renode comes with a command for inspecting RESD files without a need to load them to any particular sensor model.

To analyze the content of a RESD file, first load it with:

```
(monitor) resd load r1 @my_samples.resd
RESD file from 'my_samples.resd' loaded under identifier 'r1'
```

Now, you can print information about sample blocks with:

```
(monitor) resd list-blocks r1
Blocks in r1:
1. [00:00:00.000000..00:00:02.000000] Acceleration:0
2. [00:00:02.000000..00:01:05.500000] Acceleration:0
(monitor) resd describe-block r1 1
Index: 1
Sample type: Acceleration
Channel ID: 0
Start Time: 00:00:00.000000
End Time: 00:00:02.000000
Duration: 00:00:02.000000
Samples count: 2
Period: 00:00:01.000000
Frequency: 1Hz
```

You can also dump selected samples (e.g., between timestamps of 2.2 and 2.3 seconds) with:
```
(monitor) resd get-samples-range r1 2 "2.2" "2.3"
00:00:02.203125: [0, 0, 0.1] g
00:00:02.218750: [0, 0, 0.2] g
00:00:02.234375: [0, 0, 0.3] g
00:00:02.250000: [0, 0, 0.2] g
00:00:02.265625: [0, 0, 0.2] g
00:00:02.281250: [0, 0, 0.1] g
00:00:02.296875: [0, 0, 0.0] g
```

For more details, see the command's help output:
```
(monitor) help resd
resd
introspection for RESD files

You can use the following commands:
'resd load NAME PATH'   loads RESD file under identifier NAME
'resd unload NAME'      unloads RESD file with identifier NAME
'resd list-blocks NAME' list data blocks from RESD file with identifier NAME
'resd describe-block NAME INDEX'        show informations about INDEXth block from RESD with identifier NAME
'resd get-samples NAME INDEX "START_TIME" COUNT'        lists COUNT samples starting at START_TIME from INDEXth block of RESD with identifier NAME
'resd get-samples-range NAME INDEX "START_TIME" "DURATION"'     lists DURATION samples starting at START_TIME from INDEXth block of RESD with identifier NAME
'resd get-samples-range NAME INDEX "START_TIME..END_TIME"'      lists samples between START_TIME and END_TIME from INDEXth block of RESD with identifier NAME
'resd get-prop NAME INDEX PROP' read property PROP from INDEXth block of RESD with identifier NAME
  possible values for PROP are: SampleType, ChannelID, StartTime, EndTime, Duration, SamplesCount
```

