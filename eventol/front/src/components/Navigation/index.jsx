import React from 'react';

import './index.scss';


export default class Navigation extends React.PureComponent {
  handleSearchFocus = event => {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('search-input').focus(); // TODO: move to utils
  }

  render(){
    return (
      <div className='navigation' id='navigation'>
        <nav>
          <ul>
            <a onClick={this.handleSearchFocus} onKeyPress={this.handleSearchFocus} role='link' tabIndex='0'>
              <li>{gettext('Search')}</li>
            </a>
            <a href='http://eventol.github.io/eventoL/#/'><li>{gettext('Documentation')}</li></a>
            {/* TODO: move link to utils */}
            <a href='#featured'><li>{gettext('Featured')}</li></a>
            <a href='#recent'><li>{gettext('Recent')}</li></a>
            <a href='/report'><li>{gettext('Generic report')}</li></a>
          </ul>
        </nav>
      </div>
    );
  }
}
