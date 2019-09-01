import React from 'react';
import renderer from 'react-test-renderer';

import ItemMap from '.';

import {event1} from '../../utils/__mock__/data';

describe('ItemMap', () => {
  let component;
  let sliderId;
  let tree;

  const getComponent = () => {
    component = renderer.create(<ItemMap sliderId={sliderId} {...event1} />);
    return component;
  };

  beforeEach(() => {
    sliderId = event1.id.toString();
    const id = `${sliderId}${event1.eventSlug}`;
    document.body.innerHTML = `<div><div id="${id}">Map</div></div>`;
    component = getComponent();
    tree = component.toJSON();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });
});
