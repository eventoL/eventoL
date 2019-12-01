import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../../utils/logger', () => ({log: jest.fn()}));

import Arrow from '.';

describe('Arrow', () => {
  let component;
  let tree;
  let onClickSpy;
  let event;

  beforeEach(() => {
    onClickSpy = jest.fn();
    event = {
      preventDefault: jest.fn(),
      stopPropagation: jest.fn(),
    };
    component = renderer.create(<Arrow onClick={onClickSpy} type="prev" />);
    tree = component.toJSON();
  });

  describe('Snapshots', () => {
    test('Default', () => {
      expect(tree).toMatchSnapshot();
    });

    test('prev', () => {
      component = renderer.create(<Arrow type="prev" />);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });

    test('next', () => {
      component = renderer.create(<Arrow type="next" />);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });

    test('another type', () => {
      component = renderer.create(<Arrow type="another" />);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });

    test('with custom style', () => {
      component = renderer.create(
        <Arrow style={{padding: '10px'}} type="prev" />
      );
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });
  });

  test('should call onClick handle', () => {
    tree.props.onClick(event);
    expect(event.preventDefault).toBeCalled();
    expect(event.stopPropagation).toBeCalled();
    expect(onClickSpy).toBeCalled();
  });
});
