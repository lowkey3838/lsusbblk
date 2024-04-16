# lsusbblk

**lsusbblk** is the result of a personal itch to simplify know more about the attached
usb block devices (*usb memmory sticks or disks*) that has been connected to the computer.
The ultimate goal has been to identify the device and what the device claimes to be, as 
opposed to, what the device has negotiated with the operating system.

The application is a command line utility that displays information to the user about the
connected usb block devices. It can also be used to wait for the next device to be attached.
This can be very usefull is you intend to do some destructive operation on the device such as 
a reformating.

The application is also created to be easy to utilise in shell scripting.

# Usage example
```bash
user@computer:~/$ lsusbblk -l
 
DEVICE   | USBVER  | VENDOR | MODEL   | ID        | SIZE | SERIAL       | LABEL | 
-------- + ------- + ------ + ------- + --------- + ---- + ------------ + ----- + 
/dev/sdd | USB 3.2 | ROG    | ESD-S1C | 0b05:1932 | 0    | MBD0AP009494 | None  | 
```

# Application installation

## Application dependencies

python3-colorama
python3-pyusb

# Development setup

'sudo dnf install @development-tools rpmdevtools'



