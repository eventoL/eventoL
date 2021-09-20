import React from 'react';
import PropTypes from 'prop-types';

import {PROFILE_URL} from '../../utils/urls';

import './index.scss';

const UserProfile = ({user: {first_name: firstName, last_name: lastName}}) => (
  <div className="user-profile">
    <a href={PROFILE_URL}>
      <div className="user">
        <div className="name">{`${firstName} ${lastName}`}</div>

        <div className="image">
          <div className="fa fa-user fa-2x" />
        </div>
      </div>
    </a>
  </div>
);

UserProfile.propTypes = {
  user: PropTypes.shape({
    first_name: PropTypes.string,
    last_name: PropTypes.string,
  }).isRequired,
};

export default UserProfile;
