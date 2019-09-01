import React from 'react';
import renderer from 'react-test-renderer';

import SignIn from '.';

describe('SignIn', () => {
  let component;
  let tree;

  const getComponent = () => {
    component = renderer.create(<SignIn />);
    return component;
  };

  beforeEach(() => {
    component = getComponent();
    tree = component.toJSON();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });
});
