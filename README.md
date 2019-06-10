# mailWatch
Python program to check Microsoft exchange mail.
## Dependencies
Exchangelib, html2text and getkey are necessary to run this program.
```
pip install exchangelib html2text getkey
```
## Configuration
A config file named **config.ini** is necessary for this program to work with the following contents:
```
[DEFAULT]
USER = your email address
PASSWORD = your password
REFRESH = 300 < amount of time in seconds to refresh
```

For now the config must be on the same folder as the script.


Future features include:

* Daemon mode: simply run on the background and notify of new email
* Open email items to read them :heavy_check_mark:
* Multiple pages of mail
* Better UI
