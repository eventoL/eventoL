import React from 'react';
import './index.scss';


export default class Navigation extends React.Component {
  searchFocus(){
    document.getElementById('search-input').focus();
  }

  render(){
    return (
      <div id="navigation" className="NavigationNarrow">
        <nav>
          <ul>
            <li onClick={this.searchFocus}>Buscar</li>
            <li>Mi lista</li>
            <a href='#destacados'><li>Destacados</li></a>
            <a href='#destacados'><li>Recientes</li></a>
          </ul>
        </nav>
      </div>
    );
  }

};
