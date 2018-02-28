import React from 'react';
import './index.scss';


export default class Navigation extends React.Component {
  searchFocus(){
    document.getElementById('search-input').focus();
  }

  render(){
    return (
      <div className="SignIn">
        <ul>
          <li><a href='/accounts/login/'>Sign In</a></li>
          <li><a href='/accounts/signup/'>Sign Up</a></li>
        </ul>
      </div>
    );
  }

};
