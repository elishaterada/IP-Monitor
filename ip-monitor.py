#!/usr/bin/env python

"""
IP Monitor

Optionally pass IP monitoring frequency in seconds as a first argument
"""

import sys
import urllib2
from datetime import datetime
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from ConfigParser import SafeConfigParser


# Get current time in pretty format
def pretty_time():
    now = datetime.now()
    pretty_time_format = now.strftime("%Y-%m-%d %H:%M:%S")
    return pretty_time_format


# Query the content from given URL
def ip_query():
    parser = SafeConfigParser()
    parser.read('settings.cfg')
    ip_source = parser.get('ip_source', 'url')

    try:
        soup = BeautifulSoup(urllib2.urlopen(ip_source))
        ip_address = str(soup)
    except urllib2.HTTPError:
        print "There is an error with source URL"
        return

    return ip_address


# Send email notification
def send_notification(result):

    # Load and parse config file
    parser = SafeConfigParser()
    parser.read('settings.cfg')
    recipient_email = parser.get('email', 'recipient')
    gmail_user = parser.get('email', 'gmail_user')
    gmail_pwd = parser.get('email', 'gmail_pwd')

    # Create minimal message
    msg = MIMEText(result)
    msg['From'] = gmail_user
    msg['To'] = recipient_email
    msg['Subject'] = "Notification"

    # Send message
    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(gmail_user, gmail_pwd)
    mail_server.sendmail(gmail_user, recipient_email, msg.as_string())
    mail_server.close()
    return


def main(argv=None):
    if argv is None:
        argv = sys.argv

    #0 Check and parse user input
    if len(argv) < 2:
        monitor_frequency = 3600
    else:
        monitor_frequency = argv[1]

    old_ip = ip_query()

    while True:

        #1 Query for the new public IP address
        new_ip = ip_query()

        #2 Compare old and new IP address and process the result
        if old_ip is new_ip:
            continue
        else:
            current_time = pretty_time()
            result = "Your IP address is updated to " + new_ip + " at " + current_time + "\n"
            # Send email notification
            send_notification(result)
            # The updated content becomes old content for successive query
            old_ip = new_ip

        #3 Wait for specified time period
        time.sleep(int(monitor_frequency))

if __name__ == "__main__":
    sys.exit(main())
