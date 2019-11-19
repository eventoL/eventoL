import React from 'react';
import PropTypes from 'prop-types';

import Logger from '../../utils/logger';
import SliderItems from '../SliderItems';
import {getUrl} from '../../utils/api';
import {getApiFullUrl} from '../../utils/urls';
import {parseEventToItem, emptyEventItem} from '../../utils/events';

import './index.scss';


export default class TitleList extends React.Component {
  static propTypes = {
    id: PropTypes.string.isRequired,
    showEmpty: PropTypes.bool,
    title: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
  }

  static defaultProps = {
    showEmpty: false,
  }

  state = {
    data: [],
    mounted: false,
  }

  componentDidMount(){
    const {url} = this.props;
    if (url !== ''){
      this.loadContent();
      this.setState({mounted: true});
    }
  }

  componentWillReceiveProps({url}){
    const {url: prevUrl} = this.props;
    if (url !== prevUrl && url !== ''){
      this.setState({mounted: true}, () => {
        this.loadContent();
      });
    }
  }

  loadContent(){
    const {url} = this.props;
    const fullUrl = getApiFullUrl(url);
    getUrl(fullUrl)
      .then(data => this.setState({data}))
      .catch(err => Logger.error('There has been an error', err));
  }

  render(){
    const {title, id, showEmpty} = this.props;
    const {mounted, data: {results}} = this.state;
    let itemsData = '';
    if (results){
      itemsData = results.map(parseEventToItem);
    }
    if (!itemsData || itemsData.length === 0){
      if (!showEmpty) return null;
      return (
        <div className='title-list' data-loaded={mounted} id={id}>
          <div className='category-title'>
            <h1>{title}</h1>
            <SliderItems itemsData={[emptyEventItem]} sliderId={`${id}_empty`} />
          </div>
        </div>
      );
    }
    return (
      <div className='title-list' data-loaded={mounted} id={id}>
        <div className='category-title'>
          <h1>{title}</h1>
          <SliderItems itemsData={itemsData} sliderId={id} />
        </div>
      </div>
    );
  }
}
