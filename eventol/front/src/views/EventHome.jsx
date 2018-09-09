import React from 'react'
import {render} from 'react-dom'
import EventHome from '../containers/EventHome'
import {Provider} from 'react-redux'
import eventsStore from '../store/eventsStore'
import './index.scss';

const store = eventsStore();
window.render_components = properties => {
  window.params = {...properties};
  render(
    (<Provider store={store}>
      <EventHome
        background={properties.background}
        logoHeader={properties.logo_header}
        logoLanding={properties.logo_landing}
        tagMessage={properties.message}
        tagSlug={properties.tag_slug}
        user={properties.user}
      />
    </Provider>), document.getElementById('root'));
};

if (module.hot) {
  if (window.params) window.render_components(window.params);
  module.hot.accept();
}
