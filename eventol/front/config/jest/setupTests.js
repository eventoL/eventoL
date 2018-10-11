import {WebSocket} from 'mock-socket';

global.fetch = require('jest-fetch-mock');
global.WebSocket = WebSocket;
global.gettext = jest.fn(text => text);
global.$ = jest.fn();

const matchMedia = () => ({
  matches: false,
  addListener: () => {},
  removeListener: () => {},
});

window.matchMedia = window.matchMedia || matchMedia;
