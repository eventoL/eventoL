import React from 'react';
import './index.scss';


export default class Navigation extends React.Component {
  searchFocus(){
    document.getElementById('search-input').focus();
  }

  render(){
    return (
      <div id="navigation" className="Navigation">
        <nav>
          <ul>
            <li onClick={this.searchFocus}>{gettext('Search')}</li>
            <a href='http://eventol.github.io/eventoL/#/'><li>{gettext('Documentation')}</li></a>
            <a href='#featured'><li>{gettext('Featured')}</li></a>
            <a href='#recent'><li>{gettext('Recent')}</li></a>
            <a href='/report'><li>{gettext('Generic report')}</li></a>
          </ul>
        </nav>
      </div>
    );
  }
}
