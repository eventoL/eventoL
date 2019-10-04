import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../Item', () => 'Item');
jest.mock('../Slider', () => 'Slider');

import SliderItems from '.';

import {events} from '../../utils/__mock__/data';

describe('SliderItems', () => {
  let component;
  let itemsData;
  let tree;

  const getComponent = () => {
    component = renderer.create(
      <SliderItems itemsData={itemsData} sliderId="id" />
    );
    return component;
  };

  beforeEach(() => {
    itemsData = undefined;
    component = getComponent();
    tree = component.toJSON();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });

  describe('With items', () => {
    test('Snapshot', () => {
      itemsData = events;
      component = getComponent();
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });
  });
});
