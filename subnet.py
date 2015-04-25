import functools
from sys import argv


def ip2int(ip):
    """
        This function converts the string version of an ip address an integer representation.
    """
    return functools.reduce(lambda a, b: (a << 8) + b, map(int, ip.split('.')), 0)


def int2ip(n):
    """
        This function converts an integer to an ip address.
    """
    return '.'.join([str(n >> (i << 3) & 0xFF) for i in range(0, 4)[::-1]])


def subnet_ip(host, mask):
    """
        This function does a bitwise or between host and mask addresses and returns the subnet
        address.
    """
    return int2ip(ip2int(host) & ip2int(mask))


def broadcast_ip(host, mask):
    """
        This function does some bitwise arithmetic with the host and mask and returns
        the broadcast ip.
    """
    return int2ip(ip2int(host) | ~ip2int(mask))



#    Finally I read the input from standard input and print both the subnet and broadcast ip address.

print('\n'.join((
    'Subnet: {0}'.format(subnet_ip(argv[1], argv[2])),
    'Broadcast: {0}'.format(broadcast_ip(argv[1], argv[2]),
    ))))