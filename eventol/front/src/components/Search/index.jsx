import React from 'react'
import PropTypes from 'prop-types'

import './index.scss'


export default class Search extends React.Component {
  static propTypes = {
    onChange: PropTypes.func,
    onEnter: PropTypes.func
  };

  state = {
    searchTerm: ''
  }

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
      <div className='search' id='search'>
        <input
          id='search-input'
          onChange={this.handleChange}
          onKeyUp={this.handleKeyUp}
          placeholder={gettext('Search by title...')}
          type='search'
          value={searchTerm}
        />
      </div>
    );
  }
}
