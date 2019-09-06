import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../../utils/dom', () => ({
  focusOn: jest.fn(),
}));

jest.mock('../../utils/urls', () => ({
  EVENTOL_DOCUMENTATION: 'EVENTOL_DOCUMENTATION',
  REPORT_URL: 'REPORT_URL',
}));

import Navigation from '.';
import DOM from '../../utils/dom';

describe('Navigation', () => {
  let tree;
  let event;
  let instance;
  let component;

  const getComponent = () => {
    component = renderer.create(<Navigation />);
    instance = component.root;
    return component;
  };

  beforeEach(() => {
    event = {
      preventDefault: jest.fn(),
      stopPropagation: jest.fn(),
    };
    component = getComponent();
    tree = component.toJSON();
  });

  afterEach(() => {
    DOM.focusOn.mockClear();
  });

  test('should call event.stopPropagation, event.preventDefault and DOM.focusOn on click event', () => {
    expect(event.preventDefault).not.toBeCalled();
    expect(event.stopPropagation).not.toBeCalled();
    expect(DOM.focusOn).not.toBeCalled();

    instance.findByType('button').props.onClick(event);

    expect(event.preventDefault).toBeCalled();
    expect(event.stopPropagation).toBeCalled();
    expect(DOM.focusOn).toBeCalled();
  });

  test('should call event.stopPropagation, event.preventDefault and DOM.focusOn on key press event', () => {
    expect(event.preventDefault).not.toBeCalled();
    expect(event.stopPropagation).not.toBeCalled();
    expect(DOM.focusOn).not.toBeCalled();

    instance.findByType('button').props.onKeyPress(event);

    expect(event.preventDefault).toBeCalled();
    expect(event.stopPropagation).toBeCalled();
    expect(DOM.focusOn).toBeCalled();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });
});
