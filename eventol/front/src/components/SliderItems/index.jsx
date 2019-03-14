import React from 'react';
import PropTypes from 'prop-types';
import Slider from '../Slider';

import Item from '../Item';

export default class SliderItems extends React.PureComponent {
  static propTypes = {
    itemsData: PropTypes.arrayOf(PropTypes.object),
    sliderId: PropTypes.string.isRequired,
  };

  static defaultProps = {
    itemsData: [],
  };

  getItem = itemData => {
    const {sliderId} = this.props;
    return (
      <div key={itemData.key}>
        <Item sliderId={sliderId} {...itemData} />
      </div>
    );
  }

  render(){
    const {itemsData} = this.props;
    let items = '';
    if (itemsData){
      items = itemsData.map(this.getItem);
    }
    return <Slider>{items}</Slider>;
  }
}
