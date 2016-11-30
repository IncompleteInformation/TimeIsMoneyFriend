from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from TimeIsMoneyFriend import AuctionHouse


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Time is Money'

class SheetsSession:
    def __init__(self, credentials, http, discoveryUrl, service, spreadsheetId):
        self.credentials = credentials
        self.http = http
        self.discoveryUrl = discoveryUrl
        self.service = service
        self.spreadsheetId = spreadsheetId

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def createShoppingList(sheetsSession, auctionHouse):
    rangeName = 'Manual Info!A2:A'
    result = sheetsSession.service.spreadsheets().values().get(
        spreadsheetId=sheetsSession.spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    shopping_list = []

    for row in values:
        item_id = auctionHouse.get_item_id(row[0])
        shopping_list.append((row[0], item_id, None))
        if item_id != -1:
            print("%i %s" % (item_id, row[0]))

    return shopping_list


def writeData(sheetsSession):
    # rangeName = 'Manual Info!A2:A'
    rangeName = 'phptest'
    values = [
        ["time","is","money","friend!"],
        [7,8,9,10,11,12]
    ]
    body = {
        'range': rangeName,
        'majorDimension': 'COLUMNS',
        'values': values
    }
    sheetsSession.service.spreadsheets().values().update(
        spreadsheetId=sheetsSession.spreadsheetId, range=rangeName,
        valueInputOption='USER_ENTERED', body=body).execute()


def main():
    """ 'Time is Money, Friend!' spreadsheet URL:
    https://docs.google.com/spreadsheets/d/1nxeLFMeKLHu-EtHpYz4XL0woNEkyK3coXHZ6CSQV9UA/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1nxeLFMeKLHu-EtHpYz4XL0woNEkyK3coXHZ6CSQV9UA'

    sheetsSession = SheetsSession(credentials, http, discoveryUrl, service, spreadsheetId)

    # WARNING: slow operation
    print("fetching ALL AH data now! (feel free to interrupt)")
    #data = ah.get_whole_ah()
    filtered_ah = []

    ah = AuctionHouse()

    shopping_list = createShoppingList(sheetsSession, ah)
    writeData(sheetsSession)

if __name__ == '__main__':
    main()