import {focusOn, mapSizesToProps} from './dom';
import {MOBILE_WIDTH} from './constants';

describe('DOM utils', () => {
  const id = 'search';
  let getElementById;

  beforeEach(() => {
    document.body.innerHTML = `<div><div id="${id}">Search</div></div>`;
    getElementById = jest.spyOn(document, 'getElementById');
  });

  afterEach(() => {
    getElementById.mockRestore();
  });

  describe('focusOn', () => {
    test('should call getElementById with id', () => {
      focusOn(id);

      expect(getElementById).toBeCalled();
      expect(getElementById).toBeCalledWith(id);
    });

    test('should call element focus', () => {
      const focus = jest.fn();
      getElementById.mockImplementation(() => ({focus}));

      focusOn(id);

      expect(focus).toBeCalled();
    });
  });

  describe('mapSizesToProps', () => {
    test('should return isMobile: true when width < MOBILE_WIDTH', () => {
      const {isMobile} = mapSizesToProps({width: MOBILE_WIDTH - 1});
      expect(isMobile).toBeTruthy();
    });

    test('should return isMobile: false when width > MOBILE_WIDTH', () => {
      const {isMobile} = mapSizesToProps({width: MOBILE_WIDTH + 1});
      expect(isMobile).toBeFalsy();
    });

    test('should return isMobile: false when width === MOBILE_WIDTH', () => {
      const {isMobile} = mapSizesToProps({width: MOBILE_WIDTH});
      expect(isMobile).toBeFalsy();
    });
  });
});
