import _ from 'lodash';
import React, {useState, useEffect, useCallback} from 'react';
import PropTypes from 'prop-types';

import SliderItems from '../SliderItems';
import {getUrl} from '../../utils/api';
import {getApiFullUrl} from '../../utils/urls';
import {parseEventToItem, emptyEventItem} from '../../utils/events';

import './index.scss';

const TitleList = props => {
  const [data, setData] = useState({results: []});
  const [mounted, setMounted] = useState(false);
  const {title, id, showEmpty, url} = props;

  const loadContent = useCallback(() => {
    const fullUrl = getApiFullUrl(url);
    getUrl(fullUrl).then(setData);
  }, [url, setData]);

  useEffect(() => {
    if (!_.isEmpty(url)) {
      setMounted(true);
      loadContent();
    }
  }, [loadContent, setMounted, url]);

  const {results} = data;
  let itemsData = '';
  if (results) {
    itemsData = results.map(parseEventToItem);
  }
  if (_.isEmpty(itemsData)) {
    if (!showEmpty) return null;
    return (
      <div className="title-list" data-loaded={mounted} id={id}>
        <div className="category-title">
          <h1>{title}</h1>
          <SliderItems itemsData={[emptyEventItem]} sliderId={`${id}_empty`} />
        </div>
      </div>
    );
  }
  return (
    <div className="title-list" data-loaded={mounted} id={id}>
      <div className="category-title">
        <h1>{title}</h1>
        <SliderItems itemsData={itemsData} sliderId={id} />
      </div>
    </div>
  );
};

TitleList.propTypes = {
  id: PropTypes.string.isRequired,
  showEmpty: PropTypes.bool,
  title: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
};

TitleList.defaultProps = {
  showEmpty: false,
};

export default TitleList;
