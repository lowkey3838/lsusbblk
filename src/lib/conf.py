"""
This module provides a class that parses and updates the default values with the 
values give from the command line.
"""

from dataclasses import dataclass
from argparse import ArgumentParser

# class CustomArgumentParser(ArgumentParser):
#     def print_help(self, file=None):
#         # # Custom help message
#         # custom_help = """
#         # Custom Help Message:
#         # ====================
#         # This is a custom help message for your program.
#         # You can add your own detailed description and usage instructions here.
#         # """
#         # self._print_message(custom_help + "\n", file)
#
#         # print(self.__dict__)
#         # print(self.__dict__["_actions"])
#


@dataclass
class conf:
    """Parsing and storing command line swithes and options"""

    name: str
    version: str
    author: str
    copyright: str

    def __post_init__(self):
        """Customised command line configuration"""

        # ap = CustomArgumentParser(
        ap = ArgumentParser(
            description=f"{self.name} {self.version} options and swithes",
            epilog=f"{self.author} {self.copyright}",
        )

        # Behaviour switches
        beh = ap.add_argument_group("behaviour switches")
        add = beh.add_argument
        add("-V", "--version", help="Program version", action="store_true")
        add("-L", "--list", help="Lists available properties", action="store_true")
        add("-N", "--nodevices", help="Number of devices", action="store_true")
        add("-u", "--usblist", help="Download USB id list", action="store_true")
        add("-f", "--follow", help="Wait for new device", action="store_true")

        # Presentation switches
        pre = ap.add_argument_group("presentation switches")
        add = pre.add_argument
        add("-l", "--long", help="Long output", action="store_true")
        add("-q", "--quiet", help="Quiet output", action="store_true")
        add("-v", "--verbose", help="Verbose output", action="store_true")
        add("-s", "--scientific", help="Non-human friendly", action="store_true")
        add("-J", "--json", help="Display out in JSON", action="store_true")
        add("-M", "--monochrome", help="Display monochrome text", action="store_true")
        add("--debug", "-d", help="Debug", action="store_true")

        prv = ap.add_argument_group("presentation values")
        add = prv.add_argument
        add("-D", "--device", help="Display device", type=str)
        add("-p", "--properties", help="List of properties to display", type=str)

        # Do the actual argument parsing and store the result
        args = ap.parse_args()

        # store the parsed arguments in the dataclass
        for key, value in vars(args).items():
            setattr(self, key, value)


if __name__ == "__main__":

    print("test test")
    c = conf(name="my_app", version="1.2.3", author="lowkey", copyright="yepp mine")
    print(c.name)
    print(c.__dict__)
    print(f"{c.debug=}")
    print(f"{dir(c)=}")
