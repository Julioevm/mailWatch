from exchangelib import DELEGATE, Account, Credentials, Folder
import configparser

USER = ''
PASSWORD = ''
REFRESH = 300
CREDENTIALS = ()
ACCOUNT = ()

READC = '\33[34m'
UNREADC = '\033[0m'
TIME_FORMAT = '%d/%m/%Y %H:%M'

def loadConfig():
    
    global USER
    global PASSWORD
    global REFRESH

    config = configparser.ConfigParser()
    config.read('config.ini')

    USER = config['DEFAULT']['USER']
    PASSWORD = config['DEFAULT']['PASSWORD']
    refresh = int(config['DEFAULT']['REFRESH'])

    if refresh > 0 and refresh < 3000:
        REFRESH = refresh


def setAccount(USER, PASSWORD):

    global CREDENTIALS
    global ACCOUNT

    CREDENTIALS = Credentials(
        username=USER,
        password=PASSWORD
    )

    ACCOUNT = Account(
        primary_smtp_address=USER,
        credentials=CREDENTIALS, 
        autodiscover=True, 
        access_type=DELEGATE
    )

def main():
    
    loadConfig()
    setAccount(USER, PASSWORD)

    inbox = ACCOUNT.root / 'Top of Information Store' / 'Inbox'

    print('Unread email:' + str(inbox.unread_count))

    print('Last 10 emails received:')
    for item in inbox.all().order_by('-datetime_received')[:10]:
        if item.is_read:
            color = READC
        else:
            color = UNREADC
        
        print(color, item.subject, item.sender.name, item.datetime_received.strftime(TIME_FORMAT))


main()