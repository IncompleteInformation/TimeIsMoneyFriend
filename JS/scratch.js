// TIMF Basic Object Model
// Notes: Works with Node 7.4

let parser = require('node-ini');
let config = parser.parseSync('config.ini');
let BLIZZ_KEY = config.DEFAULT.blizz_key;
let DEFAULT_SERVER = config.DEFAULT.server;
let bnet = require('battlenet-api')(BLIZZ_KEY);
let request = require('request');

class AuctionHouse {
  constructor (server=DEFAULT_SERVER, download_data=false) {
    this.server = server
    this.data = this.get_json_uri()
  }
  get_json_uri () {
    let self = this;
    let jsonURIPromise = new Promise(
      function (resolve, reject) {
        bnet.wow.auction({origin: 'us', realm: self.server}, (e,r,b) => resolve(r))
      });
    jsonURIPromise
    .then(
      function (res) {
        let URI = res['files'][0]['url']
        self.get_json(URI)
      })
    .catch(
      function(reason) {
        console.log('Handle rejected promise ('+reason+') here.');
      });
    }

  get_json (URI) {
    let self = this;
    let jsonPromise = new Promise(
      function (resolve, reject) {
        request(URI, (e,r,b) => resolve(r))
      });
    jsonPromise
    .then(
      function (JSON) {
        console.log(JSON)
      })
    .catch(
      function(reason) {
        console.log('Handle rejected promise ('+reason+') here.');
      });
  }



  cb_getURI(e,r,b){
    this.jsonURI = r['files'][0]['url']
  }
  getJson(URI){
    request(URI,cb_getJSON)
  }
  cb_getJSON(e,r,b){

  }

  save_json_to_disk(json_data) {
    timestr = time.strftime("%Y.%m.%d-%H%M%S")
    dirname = "./Auction Data/%s/" % this.server
    filename = dirname + ("%s.json" % timestr)

    if (!os.path.exists(dirname)){
        os.makedirs(dirname)
      }
    let outfile = open(filename, 'w')
    json.dump(json_data, outfile, sort_keys=True, indent=4)
  }
  get_item_name(item_id) {
    item_name = bnet.item(item_id)['name']
    return item_name
  }
  get_item_id(item_name) {
    sql = `SELECT * FROM tblDBCItem WHERE name_enus = "%s" ` % item_name
    result = -1
    cursor.execute(sql)

    db_row = cursor.fetchone()  // fetch one result of SQL query (should only return 1 row anyway)

    if (db_row){
      result = db_row[0]  // first column of db is item id
    }
    else {
      console.log("\t'%s' not found in item DB. Perhaps not an exact name match?" % item_name)
    }

    return result
  }
  filter_by_item_id(item_id) {
    results = []
    for (let auction of this.data['auctions']){
      if (item_id == auction['item'] && auction['buyout']){
        results.append(auction)
      }
    }

    return results
  }
  calcStat(item_id, preferred_stat='min') {
    filtered_ah = this.filter_by_item_id(item_id)
    // prices_only = [auction['buyout'] for auction in filtered_ah]
    prices_only = Array.from(filtered_ah, auction => auction['buyout'])
    num_listings = len(prices_only)
    market_volume = sum(prices_only)
    if (num_listings > 0){
      mean_buyout = market_volume/num_listings/10000
      min_buyout = min(prices_only)/10000
    }
    else{
      mean_buyout = 0
      min_buyout = 0
    }

    results = {'count': num_listings, 'mean': mean_buyout, 'min': min_buyout}

    return results[preferred_stat]
    }
  };
// class Item {
//   constructor (ID, name) {
//     this.itemID       = ID;
//     this.spellName    = name;
//     this.AHValue      = 0;
//     this.vendorValue  = 0;
//     this.cost         = new Set();
//     this.value        = new Set();
//     this.updated      = 0;
//   }
// };
//
// class Recipe {
//   constructor (ID, name, castTime = 1.5) {
//     this.spellID    = ID;
//     this.spellName  = name;
//     this.inputs     = new Map();  //KVP <int itemID, int quantity>
//     this.outputs    = new Map();  //KVP <int itemID, double quantity>
//     this.castTime   = castTime;
//   }
// };

//Builds set of spells involved in the cost or value of an item
//Set<spell> (int itemID, String direction, Set<recipe> recipes)
function findRelatedSpells (item, direction, recipes) {
  let foundRecipes = new Set();
  for (let recipe of recipes) {
    if (recipe[direction].has(item.itemID)){
      foundSpells.add(recipe);
    }
  }
  return foundRecipes;
}

//Dig until you hit items that are not craftable (or reach a cycle which is yet undetermined)
function findRawMats (item) {};

//Create and test connection
let mysql      = require('mysql');
let connection = mysql.createConnection({
  host     : 'newswire.theunderminejournal.com',
  database : 'newsstand'
});


function buildSpellMap() {
  let spellMap = new Map();
  let query = `SELECT DISTINCT id,name FROM tblDBCSpell INNER JOIN tblDBCItemReagents ON tblDBCSpell.id=tblDBCItemReagents.spell`;

  return new Promise((resolve,reject) => {
    connection.query(query, (error, results) => {

      if (error) reject(error);

      for (let result of results){
        spellMap.set(result.id, result.name);
      }
      resolve(spellMap);
    })
  })
}

function SQL_CONNECT_AND_WORK() {
  connection.connect();

  let spellSet = buildSpellMap()
    .then(res => console.log(res))
    .catch(e => console.log(e));

  connection.end();
}

function resolutionAsParameter(resolved){
  resolved.then(x => makeMorePromises(x));
}

let ah = new AuctionHouse();
//SQL_CONNECT_AND_WORK();
