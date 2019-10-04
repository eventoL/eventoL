import React from 'react';
import renderer from 'react-test-renderer';

import Title from '.';

describe('Title', () => {
  let component;
  let label;
  let tree;

  const getComponent = () => {
    component = renderer.create(<Title label={label} />);
    return component;
  };

  beforeEach(() => {
    label = undefined;
    component = getComponent();
    tree = component.toJSON();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });

  describe('With data', () => {
    test('Snapshot', () => {
      label = 'label';
      component = getComponent();
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });
  });
});
