from functools import partial
import shutil
from colorama import Fore
import typing


class formated_print:

    def __init__(self, mono: bool = False, quiet: bool = False):
        columns, rows = shutil.get_terminal_size()
        self.rows: int = int(rows)
        self.columns: int = int(columns)
        self.quiet: bool = quiet
        self.mono: bool = mono

        error = partial(
            self.print_formated_string, colour=self.red, mono=mono, quiet=quiet
        )
        setattr(self, "error", error)
        warning = partial(
            self.print_formated_string, colour=self.yellow, mono=mono, quiet=quiet
        )
        setattr(self, "warning", warning)
        normal = partial(
            self.print_formated_string, colour=self.green, mono=mono, quiet=quiet
        )
        setattr(self, "normal", normal)

    # These placeholder methods help IDE to find methods actually created in __init__
    # type: ignore
    def error(self, line: str): ...  # type: ignore
    def warning(self, line: str): ...
    def normal(self, line: str): ...

    def print_formated_string(
        self, line: str, colour: typing.Callable, mono: bool, quiet: bool
    ):
        if not quiet:
            if mono:
                self.p(line)
            else:
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
        return Fore.BLUE + line + Fore.RESET

    def red(self, line):
        return Fore.RED + line + Fore.RESET

    def green(self, line):
        return Fore.GREEN + line + Fore.RESET

    def yellow(self, line):
        return Fore.YELLOW + line + Fore.RESET

    def magenta(self, line):
        return Fore.MAGENTA + line + Fore.RESET

    def cyan(self, line):
        return Fore.CYAN + line + Fore.RESET

    def reset(self, line):
        return Fore.RESET + line

    # def quiet(self, line):
    #     """if quiet return empty string"""
    #     if args.quiet:
    #         return ""
    #     else:
    #         return line
    #
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

    def col(self, lable, label_size, div):
        """format column string"""
        return self.label(lable, label_size, "l", div)

    def print_line(self, property, property_size, value, i):
        """present property line"""
        tmpl = "{:<" + "{}".format(str(property_size)) + "} : "
        self.p(
            " " * i
            + self.green(tmpl.format(property.upper()))
            + self.yellow(str(value))
        )


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

    e = formated_print()
    e.normal("Test normal")
    f = formated_print(mono=True)
    f.normal("Test normal")
    g = formated_print(quiet=True)
    g.normal("Test normal")

    a.print_line("SSIZE", 25, "2222", 5)
