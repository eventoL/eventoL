import React from 'react';
import {WebSocket} from 'mock-socket';

global.$ = jest.fn();
global.WebSocket = WebSocket;
global.gettext = jest.fn(text => text);
global.fetch = require('jest-fetch-mock');

const matchMedia = () => ({
  matches: false,
  addListener: () => {},
  removeListener: () => {},
});

window.matchMedia = window.matchMedia || matchMedia;
jest.mock('react-sizes', () => () => Component => props => (
  <Component {...props} />
));

global.L = {
  map: jest.fn(() => ({
    setView: jest.fn(() => ({
      attributionControl: {
        setPrefix: jest.fn(),
      },
    })),
  })),
  tileLayer: jest.fn(() => ({
    addTo: jest.fn(),
  })),
  marker: jest.fn(() => ({
    addTo: jest.fn(),
  })),
};
