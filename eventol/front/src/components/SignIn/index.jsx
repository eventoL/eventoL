import React from 'react';

import './index.scss';


export default class SignIn extends React.PureComponent {
  searchFocus = () => {
    document.getElementById('search-input').focus(); // TODO: move to utils 
  }

  render(){
    return (
      <div className='sign-in'>
        <ul>
          <li><a href='/accounts/login/'>{gettext('Sign In')}</a></li>
          <li><a href='/accounts/signup/'>{gettext('Sign Up')}</a></li>
        </ul>
      </div>
    );
  }
}
