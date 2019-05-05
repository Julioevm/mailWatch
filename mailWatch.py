from exchangelib import DELEGATE, Account, Credentials, Folder
import configparser

USER = ''
PASSWORD = ''
REFRESH = 300
CREDENTIALS = ()
ACCOUNT = ()

colors = {

        'blue': '\33[34m',
        'white': '\033[0m'
        }
TIME_FORMAT = '%d/%m/%Y %H:%M'

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'

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

def get_mail(inbox,num):

    return inbox.all().order_by('-datetime_received')[:num]

def main():
    
    loadConfig()
    setAccount(USER, PASSWORD)
    inbox = ACCOUNT.root / 'Top of Information Store' / 'Inbox'
    print('Unread email:' + str(inbox.unread_count))

    print('Last 10 emails received:')

    mails = get_mail(inbox, 10)
    i = 1
    for mail in mails:
        line = '['+str(i)+']' + ' ' + mail.datetime_received.strftime(TIME_FORMAT)+ ' ' + mail.subject + ' - ' + mail.sender.name 
        if mail.is_read:
            color = 'blue'
        else:
            color = 'white'
        
        print(colorize(line, color))
        i += 1

if __name__ == "__main__":
    main()
