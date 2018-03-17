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
            <li onClick={this.searchFocus}>Buscar</li>
            <li><a href='#destacados'>Destacados</a></li>
            <li><a href='#recientes'>Recientes</a></li>
          </ul>
        </nav>
      </div>
    );
  }

};
