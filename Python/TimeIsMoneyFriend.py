import wowapi
import urllib
import json
import ConfigParser
import MySQLdb

config = ConfigParser.ConfigParser()
config.read('./config.ini')
BLIZZ_KEY = config.get('DEFAULT', 'blizz_key')
DEFAULT_SERVER = config.get('DEFAULT', 'server')
blizzapi = wowapi.API(BLIZZ_KEY)

item_db = MySQLdb.connect(host="newswire.theunderminejournal.com", db="newsstand")
cursor = item_db.cursor()


class AuctionHouse(object):
    def __init__(self, server=DEFAULT_SERVER):
        self.server = server

    def get_whole_ah(self):
        # TODO: cache results & check new queries against last data retrieval
        auction_file = blizzapi.auction_status(self.server)
        data_url = auction_file['files'][0]['url']
        response = urllib.urlopen(data_url)
        auction_data = json.load(response)

        print(data_url)

        return auction_data

    def get_item_name(self, item_id):
        item_name = blizzapi.item(item_id)['name']
        return item_name

    def get_item_id(self, item_name):
        sql = '''SELECT * FROM `tblDBCItem` WHERE name_enus = "%s" ''' % item_name
        result = -1
        cursor.execute(sql)

        db_row = cursor.fetchone()  # fetch one result of SQL query (should only return 1 row anyway)

        if db_row:
            result = db_row[0]  # first column of db is item id
        else:
            print("\t'%s' not found in item DB. Perhaps not an exact name match?" % item_name)

        return result

