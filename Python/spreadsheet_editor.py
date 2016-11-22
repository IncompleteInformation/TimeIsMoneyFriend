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
    rangeName = 'Manual Info!A2:A'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    # Indices for removal of category names such as 'Pots' and 'Flasks' etc
    category_indices = [0, 8, 13, 21, 27, 29, 31, 35, 39, 43, 49, 55]

    shopping_list = []

    if not values:
        print('No data found.')
    else:
        for i in reversed(category_indices):
            del values[i]
        for row in values:
            # Print column A which corresponds to index 0
            print(row[0])
            shopping_list.append(str(row[0]))

    print(shopping_list)
    shopping_list_ids = [124105,124106,124101]
    filtered_ah = []

    ah = AuctionHouse()
    data = ah.get_whole_ah()

    # for auction in data['auctions']:
    #     if auction['item'] in shopping_list_ids:



if __name__ == '__main__':
    main()