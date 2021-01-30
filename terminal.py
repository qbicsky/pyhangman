# clear() function imports
import os
from subprocess import call
# terminal_size() function imports
import fcntl
import termios
import struct


def clear():
    call('clear' if os.name == 'posix' else 'cls')


def return_key():
    if(os.name == 'posix'):
        return "Return"
    else:
        return "Enter"


def size(dim):
    """
    Returns value of terminal dimensions

    Args:
        dim (str): th - terminal height, tw - terminal width

    Returns:
        int: Value of specified dimension or without argument
             - all dimensions
    """
    th, tw, hp, wp = struct.unpack('HHHH',
                                   fcntl.ioctl(0, termios.TIOCGWINSZ,
                                               struct.pack('HHHH', 0, 0, 0, 0)))
    dimensions = {'th': th, 'tw': tw, 'hp': hp, 'wp': wp}
    for dimension in dimensions:
        if(dim == dimension):
            return dimensions[dimension]
        else:
            return -1
