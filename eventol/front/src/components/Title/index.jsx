import React from 'react';
import './index.scss';


export default class Title extends React.Component {
  render(){
    const {label, children} = this.props;
    return (
      <div className='row'>
        <div className="col-sm-12">
          <div className="title"><h1>{label}</h1>
            <div className="buttons pull-right">
              {children}
            </div>
          </div>
        </div>
      </div>
    );
  }
}
