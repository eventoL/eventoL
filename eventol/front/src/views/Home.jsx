import React from 'react'
import { render } from 'react-dom'
import Home from '../containers/Home'
import {Provider} from 'react-redux'
import eventsStore from '../store/eventsStore'
import './index.css';

const store = eventsStore();
window.render_components = properties => {
  window.params = {...properties};
  render(
    (<Provider store={store}>
       <Home />
    </Provider>), document.getElementById('root'));
};

if (module.hot) {
  if (window.params) window.render_components(window.params);
  module.hot.accept();
}
