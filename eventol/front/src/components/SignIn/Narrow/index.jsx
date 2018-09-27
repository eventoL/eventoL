import React from 'react';
import './index.scss';


//TODO: merge with Signin default and move style to scss media query
export default class Navigation extends React.PureComponent {
  searchFocus(){
    document.getElementById('search-input').focus();
  }

  render(){
    return (
      <div className='sign-in-narrow'>
        <ul>
          <li><a href='/accounts/login/'>{gettext('Sign In')}</a></li>
          <li><a href='/accounts/signup/'>{gettext('Sign Up')}</a></li>
        </ul>
      </div>
    );
  }
}
