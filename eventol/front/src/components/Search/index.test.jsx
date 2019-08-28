import React from 'react';
import renderer from 'react-test-renderer';

import Search from '.';

describe('Search', () => {
  let component;
  let instance;
  let tree;

  const getComponent = () => {
    component = renderer.create(<Search />);
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
