import thunk from 'redux-thunk';
import {compose, createStore, applyMiddleware} from 'redux';

import reducer from '../reducers';

const getStore = () => {
  const middleware = compose(applyMiddleware(thunk));
  const store = createStore(reducer, middleware);
  return store;
};

export default getStore;
