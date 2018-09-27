import {compose, createStore, applyMiddleware} from 'redux';
import thunk from 'redux-thunk';
import reducer from '../reducers';


export default function linksStore() {
  const middleware = compose(applyMiddleware(thunk));
  const store = createStore(reducer, middleware);
  return store;
}
