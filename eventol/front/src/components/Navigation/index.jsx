import React from 'react';

import {focusOn} from '../../utils/dom';
import {EVENTOL_DOCUMENTATION, REPORT_URL} from '../../utils/urls';

import './index.scss';

export default class Navigation extends React.PureComponent {
  handleSearchFocus = event => {
    event.preventDefault();
    event.stopPropagation();
    focusOn('search-input');
  };

  render() {
    return (
      <div className="navigation" id="navigation">
        <nav>
          <ul>
            <button
              onClick={this.handleSearchFocus}
              onKeyPress={this.handleSearchFocus}
              role="link"
              tabIndex="0"
              type="button"
            >
              <li>{gettext('Search')}</li>
            </button>
            <a href={EVENTOL_DOCUMENTATION}>
              <li>{gettext('Documentation')}</li>
            </a>
            <a href="#featured">
              <li>{gettext('Featured')}</li>
            </a>
            <a href="#recent">
              <li>{gettext('Recent')}</li>
            </a>
            <a href={REPORT_URL}>
              <li>{gettext('Generic report')}</li>
            </a>
          </ul>
        </nav>
      </div>
    );
  }
}
