IP-Monitor
==========

*Version 0.01*

This is a python program that monitor your public IP address and notify when there is a change.
You can optionally pass monitor frequency in seconds as a first argument.
Otherwise the program will monitor for your IP once an hour.

Setup
-----

1. Add your Gmail account information in settings.cfg

2. Run the program. You can optionally pass monitoring frequency in seconds as first argument.

Notice
------

* This program is tested on Python 2.7.2
* You need BeautifulSoup installed in your Python environment
* This program will use your Gmail account to send email so your computer doesn't need to be setup to send email.
* The program fetches IP address from http://ip.42.pl/ip so this will not work when the site is down. You can always use another source to return your public IP address as long as it only returns IP address in the source.