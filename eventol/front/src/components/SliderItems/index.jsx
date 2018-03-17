import React from 'react';
import Slider from '../Slider'

import Item from '../Item';

const SliderItems = ({itemsData}) => {
  let items = '';
  if(itemsData) {
    items = itemsData.map(itemData => <div key={itemData.key}><Item {...itemData} /></div>);
  }
  return (
    <Slider>
      {items}
    </Slider>
  );
};

export default SliderItems;
