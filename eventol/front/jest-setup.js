import Enzyme from 'enzyme';
import {WebSocket} from 'mock-socket';
import Adapter from 'enzyme-adapter-react-16';

Enzyme.configure({adapter: new Adapter()});

global.$ = jest.fn();
global.WebSocket = WebSocket;
global.gettext = jest.fn(text => text);
