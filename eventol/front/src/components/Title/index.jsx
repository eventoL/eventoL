import React from 'react';
import PropTypes from 'prop-types';

import './index.scss';


const Title = ({label, children}) => (
  <div className='row'>
    <div className='col-sm-12'>
      <div className='title'>
        <h1>{label}</h1>
        <div className='buttons pull-right'>
          {children}
        </div>
      </div>
    </div>
  </div>
);

Title.propTypes = {
  label: PropTypes.string,
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]),
};

Title.defaultProps = {
  label: '',
  children: null,
};

export default Title;
