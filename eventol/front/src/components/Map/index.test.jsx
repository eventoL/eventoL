import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../../utils/logger', () => ({error: jest.fn()}));

import Map from '.';

import {event1} from '../../utils/__mock__/data';

describe('Map', () => {
  let component;
  let sliderId;
  let tree;

  const getComponent = () => {
    component = renderer.create(
      <Map
        eventSlug={event1.eventSlug}
        place={event1.place}
        sliderId={sliderId}
      >
        Children
      </Map>
    );
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
