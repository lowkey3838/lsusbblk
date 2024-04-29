from functools import partial
import shutil
from colorama import Fore

# from colorama import Fore, Back, Style
from argparse import ArgumentParser


class formated_print:

    def __init__(self, mono: bool = False, quiet: bool = False):
        columns, rows = shutil.get_terminal_size()
        self.rows = int(rows)
        self.columns = int(columns)
        self.quiet = quiet
        self.mono = mono
        error = partial(
            self.print_formated_string, colour=self.red, mono=mono, quiet=quiet
        )
        setattr(self, "error", error)
        warning = partial(
            self.print_formated_string, colour=self.yellow, mono=mono, quiet=quiet
        )
        setattr(self, "warning", warning)
        warning = partial(
            self.print_formated_string, colour=self.yellow, mono=mono, quiet=quiet
        )
        setattr(self, "warning", warning)

    def error(self, *args, **kvargs): ...
    def warning(self, *args, **kvargs): ...

    def print_formated_string(
        self, line: str, colour: callable, mono: bool, quiet: bool
    ):
        self.p(colour(line))

    def p(self, line):
        """Print line unless line empty"""

        # Minimum resulting line length is 64 character
        dots = " ... "
        l_size = max(int((self.columns - len(dots)) / 1), 30)
        r_size = max(self.columns - l_size - len(dots), 29)
        if line != "":
            if len(line) <= self.columns:
                print(line)
            else:
                # if terminal is to narrow shorten line
                print(line[:l_size] + dots + line[-r_size:])

    """ colour control """

    def blue(self, line):
        return self.monochrome(Fore.BLUE, line)

    def red(self, line):
        return self.monochrome(Fore.RED, line)

    def green(self, line):
        return self.monochrome(Fore.GREEN, line)

    def yellow(self, line):
        return self.monochrome(Fore.YELLOW, line)

    def magenta(self, line):
        return self.monochrome(Fore.MAGENTA, line)

    def cyan(self, line):
        return self.monochrome(Fore.CYAN, line)

    def reset(self, line):
        return self.monochrome(Fore.RESET, line)

    def quiet(self, line):
        """if quiet return empty string"""
        if args.quiet:
            return ""
        else:
            return line

    def monochrome(self, c, line):
        """if monochrome return clean string"""
        if self.mono:
            return line
        else:
            return c + line

    def label(self, label, size, pos, div):
        """adjust lable in fixed string"""
        if pos == "l":
            template = "{:<" + str(size) + "} " + div + " "
        else:
            template = "{:>" + str(size) + "} " + div + " "
        return template.format(label)

    def col(self, l, label_size, div):
        """format column string"""
        return self.label(l, label_size, "l", div)

    def print_line(pself, roperty, property_size, value, i):
        """present property line"""
        tmpl = "{:<" + "{}".format(str(property_size)) + "} : "
        self.p(" " * i + green(tmpl.format(property.upper())) + yellow(str(value)))


if __name__ == "__main__":
    a = formated_print()
    a.error("Test error")
    b = formated_print(mono=True)
    b.error("Test error")
    c = formated_print(quiet=True)
    c.error("Test error")

    d = formated_print()
    d.warning("Test warning")
    b = formated_print(mono=True)
    b.warning("Test warning")
    c = formated_print(quiet=True)
    c.warning("Test warning")
