import React from 'react'
import './index.scss';


export default class Search extends React.Component {
  state = {
    searchTerm: ''
  }

  handleKeyUp = event => {
    if (event.key === 'Enter') {
      const {onEnter} = this.props;
      if (onEnter) onEnter();
    }
  }

  handleChange = event => {
    const searchTerm = event.target.value;
    this.setState({searchTerm});
    const {onChange} = this.props;
    if (onChange) onChange(searchTerm);
  }

  render(){
    return (
      <div id='search' className='Search'>
        <input
          id='search-input'
          onKeyUp={this.handleKeyUp}
          onChange={this.handleChange}
          type='search'
          placeholder='Buscar por titulo...'
          value={this.state.searchTerm}/>
      </div>
    );
  }
}
