# NAME

lsusbblk - list USB block devices

# SYNOPSIS

lsusbblk \[OPTIONS\]

\[OPTIONS\]: \[-h\] \[-V\] \[-L\] \[-N\] \[-f\] \[-u\] \[-l\] \[-q\] \[-v\]
\[-s\] \[-J\] \[-M\] \[-d\] \[-D DEVICE\] \[-p PROPERTIES_LIST\]

# DESCRIPTION

**lsusbblk** is a command line program that lists attached USB block
devices such as USB memory sticks or USB external disks. The purpose of
the program is to simplify the identification of attached USB block
devices. The program has the option to wait for a device to be attached
and show device information. The program will by default display a sub
set of all available properties. The program can also be used to
retrieve a specific value or several values from a specified device.

# OPTIONS

The following options are recognized:

**\--device** DEVICE, **-D** DEVICE

    Display information only for given device.

**\--list**, **-L**

    List available properties

**\--nodevices**, **-N**

    Return number of attached USB block devices

**\--follow**, **-f**

    Display attached USB block devices and then wait for new device to
    be attached. Display the new device and then exit.

**\--usblist**, **-u**

    Download USB id list from "http://www.linux-usb.org/usb.ids". This
    list is used to match VID and PID to text representations of the
    device.

**\--verbose**, **-v**

    Display all properties of attached USB block devices.

**\--properties** PROPERTIES_LIST, **-p** PROPERTIES_LIST

    Display all properties of attached USB block devices.

**\--scientific**, **-s**

    Display device size in bytes.

**\--monochrome**, **-M**

    Display all information with monochrome text

**\--long**, **-l**

    Adds more fields to the output

**\--quiet**, **-q**

    Remove all label and support text. Only display results. Quiet
    output text in monochrome.

**\--json**, **-J**

    Remove all label and support text. Only display results in JSON.
    JSON output text in monochrome.

**\--debug**, **-d**

    This option enables debug information to be printed.

**\--version**, **-V**

    Shows the version of the program and exit.

**\--help**, **-h**, **-?**

    Displays a usage summary and exits.

# ERRORS

The program will produce an error if non-existing device is given with
the \--device parameter

# EXIT STATUS

0. Successful program execution
1. Program exited with an error

# EXAMPLES

**Default behaviour**

```bash
$ lsusbblk
```

Results in either "No USB block devices found" or a list of attached USB
block devices with default properties displayed.

**Wait for new device to be attached**

```bash
$ lsusbblk --follow
```

The program will present currently attached devices and then wait for a
new device to be attached. If a device is removed the device name will
be presented and the program will continue to wait for a new device.
When a device is detected then the device will be resented and the
program exits.

**Display selected properties**

```bash
$ lsusbblk --properties "device driver vendor_enc model_enc revision pid vid serial_long chksum"
```

The program will present currently attached devices with the given
properties.

**Display a specific property for a specific device**

```bash
$ lsusbblk --device /dev/sdc --properties "chksum" --quiet
```

The program will present the computed checksum of the devices
properties, see NOTES, and exit. This could for instance be used in a
shell script.

**Display newly inserted device by name**

```bash
$ lsusbblk -q -f -p device
```

The program waits for a newly inserted device, present the device name
and exit.

# NOTES

The property \"chksum\" is a sha256 checksum of concatenated string
representation of the following properties:

\'bus\', \'devtype\', \'type\', \'driver\', \'drive_thumb\', \'vendor\', \'vendor_enc\', \'model\', \'model_enc\', \'revision\', \'size\', \'vid\', \'pid\', \'serial\', \'serial_long\', \'interfaces\', \'interface_num\'

:

When displaying devices in the short form and the terminal is to short then the line will be truncated with \" \... \" line inserted at the middle. This is supported down to a column width of 30 characters.

:

# SECURITY

To execute this command and be able to retrieve disk size the user needs to be part of the \"disk\" group
or be executed with root privileges.

# SEE ALSO

lsblk(8), udevadm(8)

# BUGS

No known bugs. Report bugs by e-mail to the author.

# AUTHORS

Lowkey (public3838@bahnhof.se)
