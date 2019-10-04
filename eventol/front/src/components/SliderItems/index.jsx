import _ from 'lodash';
import React from 'react';
import PropTypes from 'prop-types';

import Item from '../Item';
import Slider from '../Slider';

export default class SliderItems extends React.PureComponent {
  static propTypes = {
    itemsData: PropTypes.arrayOf(
      PropTypes.shape({
        attendees: PropTypes.number,
        backdrop: PropTypes.string,
        eventSlug: PropTypes.string.isRequired,
        overview: PropTypes.string.isRequired,
        place: PropTypes.string.isRequired,
        tags: PropTypes.arrayOf(
          PropTypes.shape({
            name: PropTypes.string.isRequired,
            slug: PropTypes.string.isRequired,
          })
        ),
        title: PropTypes.string.isRequired,
        url: PropTypes.string,
      })
    ),
    sliderId: PropTypes.string.isRequired,
  };

  static defaultProps = {
    itemsData: [],
  };

  getItem = itemData => {
    const {sliderId} = this.props;
    return (
      <div key={itemData.key}>
        <Item data={itemData} sliderId={sliderId} />
      </div>
    );
  };

  render() {
    const {itemsData} = this.props;
    let items = '';
    if (!_.isEmpty(itemsData)) {
      items = itemsData.map(this.getItem);
    }
    return <Slider>{items}</Slider>;
  }
}
