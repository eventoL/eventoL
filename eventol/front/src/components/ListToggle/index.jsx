import React from 'react';

import './index.scss';

export default class ListToggle extends React.PureComponent {
  state = {toggled: false};

  handleClick() {
    const {toggled} = this.state;
    this.setState({toggled: !toggled});
  }

  render() {
    const {toggled} = this.state;
    return (
      <div
        className="list-toggle"
        data-toggled={toggled}
        onClick={this.handleClick}
        onKeyPress={this.handleClick}
        role="menuitem"
        tabIndex="0"
      >
        <div>
          <i className="fa fa-fw fa-plus" />
          <i className="fa fa-fw fa-check" />
        </div>
      </div>
    );
  }
}
