import React from 'react';

import './index.scss';


export default class Navigation extends React.PureComponent {
  handleSearchFocus(){
    document.getElementById('search-input').focus();
  }

  render(){
    return (
      <div className='navigation' id='navigation'>
        <nav>
          <ul>
            <li onClick={this.handleSearchFocus}>{gettext('Search')}</li>
            <a href='http://eventol.github.io/eventoL/#/'><li>{gettext('Documentation')}</li></a>
            {/*TODO: move link to utils*/}
            <a href='#featured'><li>{gettext('Featured')}</li></a>
            <a href='#recent'><li>{gettext('Recent')}</li></a>
            <a href='/report'><li>{gettext('Generic report')}</li></a>
          </ul>
        </nav>
      </div>
    );
  }
}
