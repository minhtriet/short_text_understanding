// singleton query builder
export default class QueryBuilder {

  static instance;
	static const base_url_address = "https://concept.research.microsoft.com/api/Concept/"
	static const base_url = new URL(base_url_address);
	static const result_number = 5;

  constructor(){
    if(instance){
      return instance;
    }

    this.instance = this;
  }
	
	generateQuery = (token) => {
		return URL(base_url, "ScoreByProb?instance={token}&topK={this.result_number}")
	}	
}

export const process = (query) => {
  tokens = query.trim().split(' ');
  for (token of tokens) {
    xhr.open("GET", url(ba"ScoreByProb?instance=apple&topK=5se, true);
  }
}
