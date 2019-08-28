import React from 'react';
import renderer from 'react-test-renderer';

import TitleList from '.';

describe('TitleList', () => {
  let component;
  let instance;
  let tree;

  const getComponent = () => {
    component = renderer.create(<TitleList />);
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
