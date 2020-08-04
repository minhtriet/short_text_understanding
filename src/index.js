import React from 'react';
import ReactDOM from 'react-dom';
import './normalize.css';
import './skeleton.css';
import './style.css';


class QueryForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {query: '', result: ''};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    fetch(`/api/v1?query=${encodeURIComponent(this.state.query)}`)
    .then(response => response.json())
    .then(
      (result) => {
        if ('error' in result) {
          this.setState({result: "No enitity found in your query"});
        }
        console.log(result)
      },
      (error) => {console.log(error)}
    );
    event.preventDefault();
  }

  handleChange(event) {
    this.setState({query: event.target.value});
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit} method="GET">
              <input id='textbox_query' value={this.state.query} onChange={this.handleChange} type='text' autoFocus/>
        </form>
        <div className="result">
          {this.state.result}
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

