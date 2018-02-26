import React from 'react';
import './index.css';


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
            <li><a href='#destacados' style={{textDecoration: 'none'}}>Destacados</a></li>
            <li><a href='#recientes' style={{textDecoration: 'none'}}>Recientes</a></li>
          </ul>
        </nav>
      </div>
    );
  }

};
