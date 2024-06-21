/* eslint-disable no-console */
import mockConsole from 'jest-mock-console';

describe('Logger utils', () => {
  const text = 'example text';
  let restoreConsole;
  let Logger;

  beforeAll(() => {
    restoreConsole = mockConsole();
    // eslint-disable-next-line global-require
    Logger = require('./logger').default;
  });

  afterAll(() => {
    restoreConsole();
  });

  test('warning', () => {
    Logger.warning(text);
    expect(console.warn).toBeCalled();
    expect(console.warn).toBeCalledWith(text);
  });

  test('error', () => {
    Logger.error(text);
    expect(console.error).toBeCalled();
    expect(console.error).toBeCalledWith(text);
  });

  test('log', () => {
    Logger.log(text);
    expect(console.log).toBeCalled();
    expect(console.log).toBeCalledWith(text);
  });
});
