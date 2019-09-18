import DOM from './dom';

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
      DOM.focusOn(id);

      expect(getElementById).toBeCalled();
      expect(getElementById).toBeCalledWith(id);
    });

    test('should call element focus', () => {
      const focus = jest.fn();
      getElementById.mockImplementation(() => ({focus}));

      DOM.focusOn(id);

      expect(focus).toBeCalled();
    });
  });
});
