import React from 'react';
import ReactDOM from 'react-dom';
import './normalize.css';
import './skeleton.css';
import './style.css';

const e = React.createElement;
const WIKIDATA_LINK = 'https://www.wikidata.org/wiki/';

class QueryForm extends React.Component {
  constructor(props) {
    super(props);
    const urlParams = new URLSearchParams(window.location.search);
    this.state = {query: urlParams.get('query') || ''};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    window.history.pushState(null, null, `?query=${encodeURIComponent(this.state.query)}`);
    fetch(`/api/v1?query=${encodeURIComponent(this.state.query)}`)
    .then(response => response.json())
    .then(
      (result) => {
        let return_dom = [];
        if ('error' in result) {
          return_dom.push(result['error']);
        } else {
          let result_index = 0;
          let i = 0;
          while (i < this.state.query.length) {
            if (result_index >= result.length || 
              i !== result[result_index]['start_pos']) {    // ran out of result or still not reach a result yet
              return_dom.push(this.state.query.charAt(i));
              i++;
            } else {
              i = result[result_index]['end_pos'] + 1;
              return_dom.push(e('a', {href: `${WIKIDATA_LINK}${result[result_index]['name']}`, key: result_index}, this.state.query.slice(result[result_index]['start_pos'], result[result_index]['end_pos'])));
              return_dom.push(e('div', {className: 'footnote', key: `${result_index}_fn`}, ` (${result[result_index]['description']}) `));
              result_index += 1;
            }
          }
        }
        ReactDOM.render(return_dom, document.getElementById('result'))
      },
      (error) => {console.log(error)}
    );
    event.preventDefault();
  }

  componentDidMount() {
    if (this.state.query) {
      this.handleSubmit(new Event('submit'));
    }
  }

  handleChange(event) {
    this.setState({query: event.target.value});
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit} method="GET">
              <input name="query" id='textbox_query' value={this.state.query} onChange={this.handleChange} type='text' autoFocus/>
        </form>
        <div id="result">
        </div>
      </div>
    );
  }
}

class App extends React.Component {
  render() {
    return (
      <div>
        <h1>nerd</h1>
        <QueryForm />
      </div>
    );
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);

