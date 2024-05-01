# lsusbblk

**lsusbblk** is the result of a personal itch to simply know more about the attached
usb block devices (*usb memmory sticks or disks*) that has been connected to the computer.
The ultimate goal has been to identify the device and what the device claimes to be, as 
opposed to, what the device has negotiated with the operating system. This is not achieved
and is possibly not achivable without adding special hardware.

The application is a command line utility that displays information to the user about the
connected usb block devices. It can also be used to wait for the next device to be attached.
This can be very usefull is you intend to do some destructive operation on the device such as 
a reformating.

The application is also created to be easy to utilise in shell scripting.

## Usage example

### Display more about the device to the user
```bash
user@computer:~/$ lsusbblk -l
 
DEVICE   | USBVER  | VENDOR | MODEL   | ID        | SIZE | SERIAL       | LABEL | 
-------- + ------- + ------ + ------- + --------- + ---- + ------------ + ----- + 
/dev/sdd | USB 3.2 | ROG    | ESD-S1C | 0b05:1932 | 0    | MBD0AP009494 | None  | 
```

### Return a JSON formated string
```bash
user@computer:~/$ lsusbblk -l -J
{"/dev/sdd":{"device":"/dev/sdd","usbver":"USB 3.2","vendor":"ROG","model":"ESD-S1C","id":"0b05:1932","size":"0","serial":"MBD0AP009494","label":"None"}}
```

### Wait for new device and display the device as a string
```bash
user@computer:~/$ lsusbblk -f -q -p device
/dev/sdd
```

# Application installation

## Application dependencies

python3-colorama
python3-pyusb
python3-flake8
python3-pylint
python3-mypy

# Development setup
Clone the git hub repository to your local repository.
```bash
git clone git@github.com:lowkey3838/lsusbblk.git
```

Create a python environment at the project level
```bash
python -m venv .
```

Setting up the build enviorment.
```bash
make setup
```

Create the build enviorment.
```bash
make
```

