import shutil
import colorama
from colorama import Fore, Back, Style
from argparse import ArgumentParser


def p(line):
    """Print line unless line empty"""

    # Minimum resulting line length is 65 character
    dots = " ... "
    l_size = max(int((columns - len(dots)) / 2), 30)
    r_size = max(columns - l_size - len(dots), 30)
    if line != "":
        if len(line) <= columns:
            print(line)
        else:
            # if terminal is to narrow shorten line
            print(line[:l_size] + dots + line[-r_size:])


def quiet(line):
    """if quiet return empty string"""
    if args.quiet:
        return ""
    else:
        return line


def monochrome(c, line):
    """if monochrome return clean string"""
    if args.monochrome:
        return line
    else:
        return c + line


""" colour control """


def blue(line):
    return monochrome(Fore.BLUE, line)


def red(line):
    return monochrome(Fore.RED, line)


def green(line):
    return monochrome(Fore.GREEN, line)


def yellow(line):
    return monochrome(Fore.YELLOW, line)


def magenta(line):
    return monochrome(Fore.MAGENTA, line)


def cyan(line):
    return monochrome(Fore.CYAN, line)


def reset(line):
    return monochrome(Fore.RESET, line)


def label(label, size, pos, div):
    """adjust lable in fixed string"""
    if pos == "l":
        template = "{:<" + str(size) + "} " + div + " "
    else:
        template = "{:>" + str(size) + "} " + div + " "
    return template.format(label)


def col(l, label_size, div):
    """format column string"""
    return label(l, label_size, "l", div)


def print_line(property, property_size, value, i):
    """present property line"""
    tmpl = "{:<" + "{}".format(str(property_size)) + "} : "
    p(" " * i + green(tmpl.format(property.upper())) + yellow(str(value)))
