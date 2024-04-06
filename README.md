# lsusbblk

lsusblk - is a command line linux tool to list block devices connected to a USB port on the computer. The tool is intended to be used interactively and also for use in scripts.

---

'lsusbblk -f'

This comnman will do a blocking wait until the user connects a usb block device, thumbdrive, to the computer and then return the device it was connected to.

The command can also be used in scripts such as bash to for an example make sure that only the most reasonly added usb block device is used in the script.

'lsusbblk -q -f'


