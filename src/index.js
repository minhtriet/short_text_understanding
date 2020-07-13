import React from 'react';
import ReactDOM from 'react-dom';
import './style.css';


class TextBoxQuery extends React.Component {
  render() {
    return (
      <input type='text'/>
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

