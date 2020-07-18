const WDK = require('wikibase-sdk');

// singleton query builder
class QueryBuilder {
  static instance;
  static wdk;
  constructor() {
    if (this.instance) {
      return this.instance;
    }
    QueryBuilder.wdk = WDK({
      instance: 'https://www.wikidata.org',
      sparqlEndpoint: 'https://query.wikidata.org/sparql'
    });
    this.instance = this;
  }

  generateURL = (token) => {
    return QueryBuilder.wdk.searchEntities(token);
  }

  getEntityInfo = (id) => {
  }
}

let queryBuilder = new QueryBuilder();
export const process = (query) => {
  let tokens = query.trim().split(' ');
  for (const token of tokens) {
    fetch(queryBuilder.generateURL(token))
      .then(response => response.json())
      .then(debugger;)

  }
}


export const getProbability = (entityID) {
  const url = wbk.getEntities({
    ids: [ 'Q647268', 'Q771376', 'Q860998', 'Q965704' ],
    language: 'en'
  });

  fetch(url)
    .then(response => response.json())
    .then(wbk.parse.wd.entities)
    .then(entities => // do your thing with those entities data)

}
