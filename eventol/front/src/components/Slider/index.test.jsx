import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('react-slick', () => 'ReactSlickSlider');
jest.mock('../Arrow', () => 'Arrow');
jest.mock('../../utils/constants', () => ({
  SLIDER_BASE_SETTINGS: {
    dots: true,
    speed: 500,
  },
}));

import Slider from '.';

describe('Slider', () => {
  let component;
  let tree;

  const getComponent = () => {
    component = renderer.create(<Slider />);
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
