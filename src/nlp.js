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
    console.log(QueryBuilder.wdk);
    return QueryBuilder.wdk.searchEntities(token);
  }
}

let queryBuilder = new QueryBuilder();
export const process = (query) => {
  let tokens = query.trim().split(' ');
  for (const token of tokens) {
    fetch(queryBuilder.generateURL(token))
      .then(function (response) {
        console.log(response);
      });
  }
}
