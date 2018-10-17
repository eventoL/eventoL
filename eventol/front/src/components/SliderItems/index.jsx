import React from 'react';
import PropTypes from 'prop-types';
import Slider from '../Slider';

import Item from '../Item';

const SliderItems = ({itemsData, sliderId}) => {
  let items = '';
  if (itemsData){
    items = itemsData.map(itemData => <div key={itemData.key}><Item sliderId={sliderId} {...itemData} /></div>); // TODO: move to function or new component
  }
  return (
    <Slider>
      {items}
    </Slider>
  );
};

SliderItems.propTypes = {
  itemsData: PropTypes.array,
  sliderId: PropTypes.string.isRequired,
};

SliderItems.defaultProps = {
  itemsData: [],
};

export default SliderItems;
