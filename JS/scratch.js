// TIMF Basic Object Model
// Notes: Works with Node 7.4
class Item {
  constructor (ID, name) {
    this.itemID       = ID;
    this.spellName    = name;
    this.AHValue      = 0;
    this.vendorValue  = 0;
    this.cost         = new Set();
    this.value        = new Set();
    this.updated      = 0;
  }
};

class Recipe {
  constructor (ID, name, castTime = 1.5) {
    this.spellID    = ID;
    this.spellName  = name;
    this.inputs     = new Map();  //KVP <int itemID, int quantity>
    this.outputs    = new Map();  //KVP <int itemID, double quantity>
    this.castTime   = castTime;
  }
};

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



function buildSpellSet(connection) {

  connection.connect();

  let spellSet = new Set();
  let query = `SELECT * FROM tblDBCItemReagents`;

  return new Promise((resolve,reject) => {

    connection.query(query, (error, results) => {

      if (error) reject(error);

      for (let result of results){
        spellSet.add(result.spell);
      }
      resolve(spellSet)
    });
    connection.end();
  });
}

function SQL_CONNECT_AND_WORK(connection) {

  buildSpellSet(connection)
    .then((res) => console.log(res.values()));

}

let connection = mysql.createConnection({
  host     : 'newswire.theunderminejournal.com',
  database : 'newsstand'
});

SQL_CONNECT_AND_WORK(connection);
/*
let r1 = new Recipe(2,"Linguini",5);
let r2 = new Recipe(4,"Food");

console.log(r1);
console.log(r2);

let i1 = new Item(45, "Hogwash Bones");

console.log(i1);
*/
