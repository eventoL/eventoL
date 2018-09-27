import React from 'react';
import {render} from 'react-dom';
import {getCommunicator} from './utils/communicator';
import Report from '../containers/Report';
import {Provider} from 'react-redux';
import eventsStore from '../store/eventsStore';
import './index.scss';

const store = eventsStore();
window.render_components = properties => {
  window.params = {...properties};
  const communicator = getCommunicator(properties);
  render(
    (
      <Provider store={store}>
        <Report communicator={communicator} eventsPrivateData={properties.events_private_data} user={properties.user} />
      </Provider>
    ), document.getElementById('root'));
};

if (module.hot) {
  if (window.params) window.render_components(window.params);
  module.hot.accept();
}
