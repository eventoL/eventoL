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
  children: PropTypes.oneOfType([
    PropTypes.array,
    PropTypes.object,
    PropTypes.element,
  ]).isRequired, // TODO: search children default proptypes
  label: PropTypes.string.isRequired,
};
