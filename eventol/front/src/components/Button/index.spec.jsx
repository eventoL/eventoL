import React from 'react';
import renderer from 'react-test-renderer';

import Button from '.';

describe('Button', () => {
  let component;
  let tree;
  let onClickSpy;
  let event;

  beforeEach(() => {
    onClickSpy = jest.fn();
    event = {
      preventDefault: jest.fn(),
      stopPropagation: jest.fn(),
      target: {
        id: 'button',
      },
    };
    component = renderer.create(<Button handleOnClick={onClickSpy} />);
    tree = component.toJSON();
  });

  test('Snapshot', () => {
    expect(tree).toMatchSnapshot();
  });

  test('should be call onClick handle', () => {
    tree.props.onClick(event);
    expect(onClickSpy).toBeCalled();
    expect(onClickSpy).toBeCalledWith('button');
  });
});
