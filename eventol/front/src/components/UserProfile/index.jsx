import React from 'react';
import PropTypes from 'prop-types';

import './index.scss';


const UserProfile = ({user: {first_name, last_name}}) => (
  <div className='user-profile'>
    <a href='/accounts/profile/'>
      <div className='user'>
        <div className='name'>{`${first_name} ${last_name}`}</div>
        <div className='image'>
          <div className='fa fa-user fa-2x' />
        </div>
      </div>
    </a>
  </div>
);

UserProfile.propTypes = {
  user: PropTypes.object //TODO: change to shape with first_name and last_name
};

export default UserProfile;
