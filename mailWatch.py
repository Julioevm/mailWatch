from exchangelib import DELEGATE, Account, Credentials, Folder
from getkey import getkey, keys
import html2text
import configparser


USER = ''
PASSWORD = ''
REFRESH = 300
CREDENTIALS = ()
ACCOUNT = ()
INBOX = ()
MAILS = []
RUN = True

colors = {
       
    'blue': '\33[34m',
    'white': '\033[0m'
}
TIME_FORMAT = '%d/%m/%Y %H:%M'


def colorize(string, color):
    if not color in colors:
        return string
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

def get_mail(inbox, num):

    return list(inbox.all().order_by('-datetime_received')[:num])


def show_mail_list(mails):
    i = 0
    for mail in mails:
        line = '['+str(i)+']' + ' ' + mail.datetime_received.strftime(
            TIME_FORMAT) + ' ' + mail.subject + ' - ' + mail.sender.name
        if mail.is_read:
            color = 'blue'
        else:
            color = 'white'

        print(colorize(line, color))
        i += 1

def show_mail(n):
    global MAILS
    mail = list(MAILS)[n]
    print(mail.subject)
    print(mail.datetime_received.strftime(TIME_FORMAT))
    print(mail.sender.name)
    # cleantext = BeautifulSoup(mail.body, "lxml").get_text()
    print(html2text.html2text(mail.body))
    input("Press Enter to continue...")

def read_key():
    global RUN
    global INBOX
    global MAILS
    key = getkey()

    if key == 'r' or key == 'R':
        print("Refreshing list.")
        MAILS = get_mail(INBOX, 10)
    elif key == 'q' or key == 'Q':
        print("Closing program. Good Bye!")
        RUN = False
    else:
        # Check for integer to select a mail
        try:
            key = int(key)
            if key >= 0 and key <= 9:
                print("Selecting item ", key)
                show_mail(key)
        except:
           print("Please enter a valid key.")


def main():

    global RUN
    global MAILS
    global INBOX

    loadConfig()
    setAccount(USER, PASSWORD)
    INBOX = ACCOUNT.root / 'Top of Information Store' / 'Inbox'
    MAILS = get_mail(INBOX, 10)

    while RUN:
        print('Unread email:' + str(INBOX.unread_count))

        print('Last 10 emails received:')

        show_mail_list(MAILS)

        print("Enter the number of item to open, R to refresh list.")
        read_key()


if __name__ == "__main__":
    main()
