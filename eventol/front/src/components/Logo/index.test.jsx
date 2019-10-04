import React from 'react';
import renderer from 'react-test-renderer';

import Logo from '.';

describe('Logo', () => {
  let component;
  let logoHeader;
  let tree;

  const getComponent = () => {
    component = renderer.create(<Logo logoHeader={logoHeader} />);
    return component;
  };

  beforeEach(() => {
    logoHeader = undefined;
    component = getComponent();
    tree = component.toJSON();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });

  describe('With custom logo', () => {
    test('Snapshot', () => {
      logoHeader = 'http://logoHeader/';
      component = getComponent();
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });
  });
});
