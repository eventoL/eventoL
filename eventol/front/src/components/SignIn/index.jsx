import React from 'react';

import DOM from '../../utils/dom';
import {LOGIN_URL, LOGOUT_URL} from '../../utils/urls';

import './index.scss';


export default class SignIn extends React.PureComponent {
  searchFocus = () => {
    DOM.focusOn('search-input');
  }

  render(){
    return (
      <div className='sign-in'>
        <ul>
          <li><a href={LOGIN_URL}>{gettext('Sign In')}</a></li>
          <li><a href={LOGOUT_URL}>{gettext('Sign Up')}</a></li>
        </ul>
      </div>
    );
  }
}
