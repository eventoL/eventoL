import React from 'react';
import PropTypes from 'prop-types';
import ItemMap from '../ItemMap';

import {getTagUrl, goToUrl} from '../../utils/urls';

import './index.scss';


export default class Item extends React.PureComponent {
  static propTypes = {
    attendees: PropTypes.number.isRequired,
    overview: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
    backdrop: PropTypes.string,
  };

  static defaultProps = {
    backdrop: null,
  };

  getTagLink = ({name, slug}) => (
    <a href={`${getTagUrl(slug)}`} key={name.toLocaleLowerCase()}>
      {name}
    </a>
  )

  goTo = () => {
    const {url} = this.props;
    goToUrl(url);
  }

  render(){
    const {
      title, attendees, overview, backdrop, tags,
    } = this.props;
    if (!backdrop) return <ItemMap {...this.props} />;
    return (
      <div className='item' style={{backgroundImage: `url(${backdrop})`}}>
        <div onClick={this.goTo} onKeyPress={this.goTo} role='button' tabIndex='0'>
          <div className='overlay'>
            <div className='title'>
              {title}
            </div>
            { attendees !== undefined && (
              <div className='rating'>
                {`${gettext('Attendees')}: ${attendees}`}
              </div>
            )}
            { tags !== undefined && (
              <div className='rating tags'>
                {/* eslint-disable-next-line react/jsx-one-expression-per-line */}
                {gettext('Tags')}: {tags.map(this.getTagLink)}
              </div>
            )}
            <div className='plot'>{overview}</div>
          </div>
        </div>
      </div>
    );
  }
}
