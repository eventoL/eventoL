import React from 'react';
import {render} from 'react-dom';
import {Provider} from 'react-redux';

import getStore from '../store';
import InstanceDetails from '../containers/InstanceDetails';

import './index.scss';

const store = getStore();

window.render_components = properties => {
  window.params = {...properties};
  render(
    <Provider store={store}>
      <InstanceDetails
        background={properties.background}
        eventolMessage={properties.message}
        events={properties.events}
        handleOnChangeLanguage={properties.onChangeLanguage}
        languages={properties.languages}
        logoHeader={properties.logo_header}
        logoLanding={properties.logo_landing}
        user={properties.user}
        users={properties.users}
        versions={properties.versions}
      />
    </Provider>,
    document.getElementById('root')
  );
};

if (module.hot) {
  if (window.params) window.render_components(window.params);
  module.hot.accept();
}
