jest.mock('./logger', () => ({
  error: jest.fn(),
  warning: jest.fn(),
  log: jest.fn(),
}));

import WsCommunicator from './WsCommunicator';

import {event1} from './__mock__/data';

describe('WsCommunicator', () => {
  let data;
  let wsUrl;
  let onOpen;
  let onClose;
  let callback;
  let reconnect;
  let onMessage;
  let communicator;
  let handleNotSupportWs;

  beforeEach(() => {
    data = event1;
    callback = jest.fn();
    handleNotSupportWs = undefined;
    onMessage = undefined;
    onClose = undefined;
    onOpen = undefined;
    reconnect = undefined;
    wsUrl = 'ws://url/';
    communicator = new WsCommunicator(
      wsUrl,
      handleNotSupportWs,
      onClose,
      onMessage,
      onOpen,
      reconnect
    );
  });

  test('Defaults', () => {
    expect(communicator.websocket).toBeInstanceOf(WebSocket);
    expect(communicator.attempts).toEqual(1);
    expect(communicator.reconnect).toEqual(true);
    expect(communicator.onOpens).toHaveLength(1);
    expect(communicator.onMessages).toHaveLength(1);
    expect(communicator.onCloses).toHaveLength(1);
    expect(communicator.handlesNotSupportWs).toHaveLength(1);
  });

  test('addOnMessage should add callback and onMessage should call this callback', () => {
    expect(communicator.onMessages).toHaveLength(1);
    expect(communicator.onMessages).not.toContain(callback);

    communicator.addOnMessage(callback);

    expect(communicator.onMessages).toHaveLength(2);
    expect(communicator.onMessages).toContain(callback);

    expect(callback).not.toBeCalled();

    communicator.onMessage(data);

    expect(callback).toBeCalled();
    expect(callback).toBeCalledWith(data);
  });

  test('addOnOpen should add callback and onOpen should call this callback', () => {
    expect(communicator.onOpens).toHaveLength(1);
    expect(communicator.onOpens).not.toContain(callback);

    communicator.addOnOpen(callback);

    expect(communicator.onOpens).toHaveLength(2);
    expect(communicator.onOpens).toContain(callback);

    expect(callback).not.toBeCalled();

    communicator.onOpen(data);

    expect(callback).toBeCalled();
    expect(callback).toBeCalledWith(data);
  });

  test('addOnClose should add callback and onClose should call this callback', () => {
    expect(communicator.onCloses).toHaveLength(1);
    expect(communicator.onCloses).not.toContain(callback);

    communicator.addOnClose(callback);

    expect(communicator.onCloses).toHaveLength(2);
    expect(communicator.onCloses).toContain(callback);

    expect(callback).not.toBeCalled();

    communicator.onClose(data);

    expect(callback).toBeCalled();
    expect(callback).toBeCalledWith(data, communicator.reconnect);
  });

  test('handlesNotSupportWs should add callback and handleNotSupportWs should call this callback', () => {
    expect(communicator.handlesNotSupportWs).toHaveLength(1);
    expect(communicator.handlesNotSupportWs).not.toContain(callback);

    communicator.addHandleNotSupportWs(callback);

    expect(communicator.handlesNotSupportWs).toHaveLength(2);
    expect(communicator.handlesNotSupportWs).toContain(callback);

    expect(callback).not.toBeCalled();

    communicator.handleNotSupportWs();

    expect(callback).toBeCalled();
  });

  test('generateInterval', () => {
    const limit = 30;
    // 1-5
    expect(communicator.generateInterval(1)).toEqual(1 * 1000);
    expect(communicator.generateInterval(2)).toEqual(3 * 1000);
    expect(communicator.generateInterval(3)).toEqual(7 * 1000);
    expect(communicator.generateInterval(4)).toEqual(15 * 1000);
    expect(communicator.generateInterval(5)).toEqual(limit * 1000);

    // 6 -> infinite
    expect(communicator.generateInterval(6)).toEqual(limit * 1000);
    expect(communicator.generateInterval(50)).toEqual(limit * 1000);
    expect(communicator.generateInterval(100)).toEqual(limit * 1000);
  });
});
