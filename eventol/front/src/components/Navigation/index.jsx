import React from 'react';
import PropTypes from 'prop-types';

import {focusOn} from '../../utils/dom';
import {EVENTOL_DOCUMENTATION, REPORT_URL} from '../../utils/urls';

import './index.scss';

export default class Navigation extends React.PureComponent {
  static propTypes = {
    handlerOnChangeLanguage: PropTypes.func.isRequired,
    languages: PropTypes.arrayOf(
      PropTypes.shape({
        code: PropTypes.string,
        name: PropTypes.string,
      })
    ),
  };

  static defaultProps = {
    languages: [],
  };

  handleSearchFocus = event => {
    event.preventDefault();
    event.stopPropagation();
    focusOn('search-input');
  };

  render() {
    const {languages, handlerOnChangeLanguage} = this.props;
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

            {languages.length > 0 && (
              <div className="languages-dropdown">
                <button className="dropbtn" type="button">
                  {gettext('Languages')}

                  <i className="fa fa-caret-down" />
                </button>

                <div className="dropdown-content">
                  {languages.map(({code, name}) => (
                    <a
                      key={code}
                      href="#lang"
                      id={code}
                      onClick={() => handlerOnChangeLanguage(code)}
                    >
                      {name}
                    </a>
                  ))}
                </div>
              </div>
            )}
          </ul>
        </nav>
      </div>
    );
  }
}
