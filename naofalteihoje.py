import sys
import getpass
import time
import smtplib
import json

from uepgwrapper import UepgWrapper

def compare_frequency(old, new):
    fields = []
    for key in old:
        if(old[key] != new[key]):
            fields.append(key)
    return fields

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit()

    config = json.load(open('config.json'))   

    username = sys.argv[1]
    password = getpass.getpass('Enter password: ')

    wrapper = UepgWrapper(username, password)

    server = smtplib.SMTP(
        config["sender_server"], 
        int(config["sender_port"])
    )

    server.ehlo(); server.starttls(); server.ehlo()
    server.login(
        config["sender_email"],
        config["sender_password"]
    )

    frequency_table_old = wrapper.parse_table_frequency()

    while(True):
        time.sleep(60)
        frequency_table = wrapper.parse_table_frequency()
        for course in compare_frequency(frequency_table_old, frequency_table):
            for receiver_email in config["receiver_emails"]:
                server.sendmail(config["sender_email"], receiver_email, f"Acabou de faltar em: {course}")
        
        frequency_table_old = frequency_table

