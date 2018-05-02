import React from 'react'
import PropTypes from 'prop-types'

import './index.scss'


export default class Search extends React.Component {
  state = {
    searchTerm: ''
  }

  propTypes = {
    onEnter: PropTypes.func,
    onChange: PropTypes.func
  };

  handleKeyUp = ({key}) => {
    if (key === 'Enter') {
      const {onEnter} = this.props;
      if (onEnter) onEnter();
    }
  }

  handleChange = ({target: {value:searchTerm}}) => {
    this.setState({searchTerm});
    const {onChange} = this.props;
    if (onChange) onChange(searchTerm);
  }

  render(){
    const {searchTerm} = this.state;
    return (
      <div id='search' className='Search'>
        <input
          id='search-input'
          onKeyUp={this.handleKeyUp}
          onChange={this.handleChange}
          type='search'
          placeholder={gettext('Search by title...')}
          value={searchTerm}/>
      </div>
    );
  }
}
