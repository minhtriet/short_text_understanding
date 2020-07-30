import React from 'react';
import ReactDOM from 'react-dom';
import './style.css';


class TextBoxQuery extends React.Component {
  constructor(props) {
    super(props);
    this.state = {query: ''};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    fetch(`/api/v1?query=${encodeURIComponent(this.state.query)}`)
    .then(response => response.json())
    .then(
      (result) => {console.log(result)},
      (error) => {console.log(error)}
    );
    event.preventDefault();
  }

  handleChange(event) {
    this.setState({query: event.target.value});
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} method="GET">
        <div id='textbox_container'>
          <input id='textbox_query' value={this.state.query} onChange={this.handleChange} type='text'/>
        </div>
      </form>
    );
  }
}

class App extends React.Component {
  render() {
    return (
      <div>
      <TextBoxQuery />
      <div className="result"></div>
      <mark> Jack </mark> is cool
      </div>
    );
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);

