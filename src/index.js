import React from 'react';
import ReactDOM from 'react-dom';
import { process } from './nlp';
import './style.css';


class TextBoxQuery extends React.Component {
  render() {
    return (
      <form onSubmit="process"  action="api/v1" method="GET">
        <input name='query' type='text'/>
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

