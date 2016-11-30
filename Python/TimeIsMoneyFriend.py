from __future__ import division
import wowapi
import urllib
import json
import ConfigParser
import MySQLdb
import time
import os

config = ConfigParser.ConfigParser()
config.read('./config.ini')
BLIZZ_KEY = config.get('DEFAULT', 'blizz_key')
DEFAULT_SERVER = config.get('DEFAULT', 'server')
blizzapi = wowapi.API(BLIZZ_KEY)

item_db = MySQLdb.connect(host="newswire.theunderminejournal.com", db="newsstand")
cursor = item_db.cursor()


class AuctionHouse(object):
    def __init__(self, server=DEFAULT_SERVER, download_data=False):
        self.server = server
        self.data = self.get_whole_ah(download_data)

    def get_whole_ah(self, save_file=False):
        # TODO: check new queries against last data retrieval
        auction_file = blizzapi.auction_status(self.server)
        data_url = auction_file['files'][0]['url']
        response = urllib.urlopen(data_url)
        auction_data = json.load(response)

        if save_file:
            self.save_json_to_disk(auction_data)
        print(data_url)

        return auction_data

    def save_json_to_disk(self, json_data):
        timestr = time.strftime("%Y.%m.%d-%H%M%S")
        dirname = "./Auction Data/%s/" % self.server
        filename = dirname + ("%s.json" % timestr)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile, sort_keys=True, indent=4)

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

    def filter_by_item_id(self, item_id):
        results = []
        for auction in self.data['auctions']:
            if item_id == auction['item'] and auction['buyout']:
                results.append(auction)

        return results

    def calcStat(self, item_id, preferred_stat='min'):
        filtered_ah = self.filter_by_item_id(item_id)
        prices_only = [auction['buyout'] for auction in filtered_ah]
        num_listings = len(prices_only)
        market_volume = sum(prices_only)
        if num_listings > 0:
            mean_buyout = market_volume/num_listings/10000
            min_buyout = min(prices_only)/10000
        else:
            mean_buyout = 0
            min_buyout = 0

        results = {'count': num_listings, 'mean': mean_buyout, 'min': min_buyout}

        return results[preferred_stat]

