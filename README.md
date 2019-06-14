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

* Auto refresh based on user timer value
* Open email items to read them :heavy_check_mark:
* Multiple pages of mail :heavy_check_mark:
* Email body paging
* Open email in editor
