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
import {focusOn} from '../../utils/dom';

describe('Navigation', () => {
  let tree;
  let event;
  let instance;
  let component;
  let languages;
  const handlerOnChangeLanguage = jest.fn();

  const getComponent = props => {
    component = renderer.create(<Navigation {...props} />);
    instance = component.root;
    return component;
  };

  beforeEach(() => {
    event = {
      preventDefault: jest.fn(),
      stopPropagation: jest.fn(),
    };
    languages = [
      {code: 'es', name: 'Spanish'},
      {code: 'en', name: 'English'},
    ];
    component = getComponent();
    tree = component.toJSON();
  });

  afterEach(() => {
    jest.clearAllMocks();
    focusOn.mockClear();
  });

  test('should call event.stopPropagation, event.preventDefault and focusOn on click event', () => {
    expect(event.preventDefault).not.toBeCalled();
    expect(event.stopPropagation).not.toBeCalled();
    expect(focusOn).not.toBeCalled();

    instance.findByType('button').props.onClick(event);

    expect(event.preventDefault).toBeCalled();
    expect(event.stopPropagation).toBeCalled();
    expect(focusOn).toBeCalled();
  });

  test('should call event.stopPropagation, event.preventDefault and focusOn on key press event', () => {
    expect(event.preventDefault).not.toBeCalled();
    expect(event.stopPropagation).not.toBeCalled();
    expect(focusOn).not.toBeCalled();

    instance.findByType('button').props.onKeyPress(event);

    expect(event.preventDefault).toBeCalled();
    expect(event.stopPropagation).toBeCalled();
    expect(focusOn).toBeCalled();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });

  describe('with languages', () => {
    beforeEach(() => {
      component = getComponent({languages, handlerOnChangeLanguage});
      tree = component.toJSON();
    });

    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });

    test('Dropdown, options and on click handlers (handlerOnChangeLanguage)', () => {
      const languagesDropdown = instance.findByProps({
        className: 'languages-dropdown',
      });

      expect(languagesDropdown).toBeDefined();

      const options = languagesDropdown.findAllByType('a');
      expect(options).toBeDefined();
      expect(options).toHaveLength(2);

      languages.forEach(({code, name}) => {
        const option = options.find(op => op.props.id === code);
        expect(option).toBeDefined();
        expect(option.children[0]).toEqual(name);

        // on Click (handlerOnChangeLanguage)
        handlerOnChangeLanguage.mockClear();

        option.props.onClick();
        expect(handlerOnChangeLanguage).toBeCalled();
        expect(handlerOnChangeLanguage).toBeCalledWith(code);
      });
    });
  });
});
