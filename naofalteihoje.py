import sys
import getpass
import time
import smtplib
from uepgwrapper import UepgWrapper

def compare_frequency(old, new):
    pass

if __name__ = '__main__':
    if len(sys.argv) < 2:
        exit()

    username = sys.argv[1]
    password = getpass.getpass('Enter password: ')

    wrapper = UepgWrapper(username, password)

    frequency_table_old = wrapper.parse_table_frequency()

    while(True):
        time.sleep(60)