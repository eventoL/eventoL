import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

import ListToggle from '.';

describe('ListToggle', () => {
  let tree;
  let element;
  let instance;
  let component;

  const getComponent = () => {
    element = <ListToggle />;
    component = renderer.create(element);
    instance = component.root;
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

    test('Snapshot with toggle change (onClick)', async () => {
      expect(tree).toMatchSnapshot();
      expect(component.getInstance().state.toggled).toBeFalsy();
      expect(
        instance.findByProps({className: 'list-toggle'}).props['data-toggled']
      ).toBeFalsy();

      instance.findByProps({className: 'list-toggle'}).props.onClick();
      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
      expect(component.getInstance().state.toggled).toBeTruthy();
      expect(
        instance.findByProps({className: 'list-toggle'}).props['data-toggled']
      ).toBeTruthy();
    });
  });
});
