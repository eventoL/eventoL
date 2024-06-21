import React from 'react';

import {LOGIN_URL, LOGOUT_URL} from '../../utils/urls';

import './index.scss';

const SignIn = () => (
  <div className="sign-in">
    <ul>
      <li>
        <a href={LOGIN_URL}>{gettext('Sign In')}</a>
      </li>

      <li>
        <a href={LOGOUT_URL}>{gettext('Sign Up')}</a>
      </li>
    </ul>
  </div>
);

export default SignIn;
