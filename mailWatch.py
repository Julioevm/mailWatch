from exchangelib import DELEGATE, Account, Credentials, Folder
from getkey import getkey, keys
import html2text
import configparser


USER = ''
PASSWORD = ''
REFRESH = 300
CREDENTIALS = ()
ACCOUNT = ()
TIME_FORMAT = '%d/%m/%Y %H:%M'
COLORS = {
       
    'blue': '\33[34m',
    'white': '\033[0m'
}


def colorize(string, color):
    if not color in COLORS:
        return string
    return COLORS[color] + string + '\033[0m'


def load_config():

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


def set_account(USER, PASSWORD):

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

def get_mail(inbox, n, m):

    return list(inbox.all().order_by('-datetime_received')[n:m])


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

def show_mail(mails, n):
    
    mail_list = list(mails)[n]
    print(mail_list.subject)
    print(mail_list.datetime_received.strftime(TIME_FORMAT))
    print(mail_list.sender.name)
    print(html2text.html2text(mail_list.body))
    input("Press Enter to continue...")

def main():

    load_config()
    set_account(USER, PASSWORD)
    inbox = ACCOUNT.root / 'Top of Information Store' / 'Inbox'
    mails = get_mail(inbox, 0, 10)
    page = 0
    max_page = inbox.total_count / 10
    unread = inbox.unread_count

    if unread > 0:
        print('Unread email:' + str(unread))

    while True:

        print('Showing page %d of %d' % (page, max_page))

        show_mail_list(mails)

        print("Enter the number of item to open, R to refresh list. N and P to load next or previous page.")
        key = getkey()

        if key == 'r' or key == 'R':
            print("Refreshing list.")
            page = 0
            mails = get_mail(inbox, 0, 10)
        elif key == 'q' or key == 'Q':
            print("Closing program. Good Bye!")
            return False
        elif key == 'n' or key == 'N':
            if page < max_page:
                print('Loading next page of emails.')
                page += 1
                mails = get_mail(inbox, page * 10, page * 10 + 10)
        elif key == 'p' or key == 'P':
            if page > 0:
                print('Loading next previous of emails.')
                page -= 1
                mails = get_mail(inbox, page * 10, page * 10 + 10)
        else:
            # Check for integer to select a mail
            try:
                key = int(key)
                if key >= 0 and key <= 9:
                    print("Opening email ", key)
                    show_mail(mails, key)
            except:
                print("Please enter a valid key.")


if __name__ == "__main__":
    main()
