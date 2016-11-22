import wowapi
import urllib
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('./config.ini')
BLIZZ_KEY = config.get('DEFAULT', 'blizz_key')
DEFAULT_SERVER = config.get('DEFAULT', 'server')
api = wowapi.API(BLIZZ_KEY)


class AuctionHouse(object):
    def __init__(self, server=DEFAULT_SERVER):
        self.server = server

    def get_whole_ah(self):
        auction_file = api.auction_status(self.server)
        data_url = auction_file['files'][0]['url']
        response = urllib.urlopen(data_url)
        auction_data = json.load(response)

        print(data_url)

        return auction_data

    def get_item_name(self, item_id):
        item_name = api.item(item_id)['name']
        return item_name

    def get_item_id(self, item_name):
        return True

