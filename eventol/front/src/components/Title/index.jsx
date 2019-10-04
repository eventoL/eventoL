import React from 'react';
import PropTypes from 'prop-types';

import './index.scss';

const Title = ({label, children}) => (
  <div className="row">
    <div className="col-sm-12">
      <div className="title">
        <h1>{label}</h1>
        <div className="buttons pull-right">{children}</div>
      </div>
    </div>
  </div>
);

Title.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]),
  label: PropTypes.string,
};

Title.defaultProps = {
  children: null,
  label: '',
};

export default Title;
