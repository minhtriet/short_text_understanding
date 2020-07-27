import React from 'react';
import ReactDOM from 'react-dom';
import { process } from './nlp';
import './style.css';


class TextBoxQuery extends React.Component {
  constructor(props) {
    super(props);
    this.state = {query: ''};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    fetch("/api/v1", this.state).then(response => console.log(response));
    event.preventDefault();
  }

  handleChange(event) {
    this.setState({query: event.target.value});
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} method="GET">
        <input value={this.state.query} onChange={this.handleChange} type='text'/>
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
      </div>
    );
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);

