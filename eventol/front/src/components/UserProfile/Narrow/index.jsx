import React from 'react'
import PropTypes from 'prop-types'

import './index.scss'


const UserProfile = ({user}) => (
  <div className='user-profile-narrow'>
    <a href='/accounts/profile/'>
        <div className="name">{user.first_name} {user.last_name}</div>
        <div className="image">
          <div className="fa fa-user fa-2x" />
      <div className='user'>
        </div>
      </div>
    </a>
  </div>
);

UserProfile.propTypes = {
  user: PropTypes.object
};

export default UserProfile;
