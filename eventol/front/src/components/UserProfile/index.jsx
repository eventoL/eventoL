import React from 'react';
import './index.scss';


const UserProfile = () => (
  <div className="UserProfile">
    <a href='/accounts/profile/' style={{textDecoration: 'none'}}>
      <div className="User">
        <div className="name">Federico Gonzalez</div>
        <div className="image">
          <img src="https://lh3.googleusercontent.com/-L9sUzpq9dXo/AAAAAAAAAAI/AAAAAAAAAAA/AFiYof3VquGCDqIIOgcCoqRuuAYGPX7mlQ/s32-c-mo/photo.jpg" alt="profile" />
        </div>
      </div>
    </a>
  </div>
);

export default UserProfile;
