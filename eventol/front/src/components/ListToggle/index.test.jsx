import React from 'react';
import renderer from 'react-test-renderer';

import ListToggle from '.';

describe('ListToggle', () => {
  let component;
  let instance;
  let tree;

  const getComponent = () => {
    component = renderer.create(<ListToggle />);
    return component;
  };

  beforeEach(() => {
    component = getComponent();
    instance = renderer.root;
    tree = component.toJSON();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });
});
