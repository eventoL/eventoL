import React from 'react';
import Slider from '../Slider'

import Item from '../Item';

const SliderItems = ({itemsData, sliderId}) => {
  let items = '';
  if(itemsData) {
    items = itemsData.map(itemData => <div key={itemData.key}><Item sliderId={sliderId} {...itemData}/></div>);
  }
  return (
    <Slider>
      {items}
    </Slider>
  );
};

export default SliderItems;
