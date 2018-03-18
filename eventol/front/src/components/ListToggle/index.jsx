import React from 'react';
import './index.scss';


export default class ListToggle extends React.Component {
  state = { toggled: false };

  handleClick(){
    const {toggled} = this.state;
    this.setState({ toggled: !toggled });
  }

  render(){
    const {toggled} = this.state;
    return (
      <div onClick={this.handleClick} data-toggled={toggled} className="ListToggle">
        <div>
          <i className="fa fa-fw fa-plus"></i>
          <i className="fa fa-fw fa-check"></i>
        </div>
      </div>
    );
  }
};
