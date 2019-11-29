import React from 'react';
import {render} from 'react-dom';
import {Provider} from 'react-redux';

import getStore from '../store';
import Home from '../containers/Home';

import './index.scss';

const store = getStore();

window.render_components = properties => {
  window.params = {...properties};
  render(
    <Provider store={store}>
      <Home
        background={properties.background}
        eventolMessage={properties.message}
        handleOnChangeLanguage={properties.onChangeLanguage}
        languages={properties.languages}
        logoHeader={properties.logo_header}
        logoLanding={properties.logo_landing}
        user={properties.user}
      />
    </Provider>,
    document.getElementById('root')
  );
};

if (module.hot) {
  if (window.params) window.render_components(window.params);
  module.hot.accept();
}
