import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../../utils/map', () => ({
  getMapId: jest.fn().mockReturnValue('mapId'),
  loadMap: jest.fn(),
}));
import {getMapId, loadMap} from '../../utils/map';

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
    document.body.innerHTML = '<div id="mapId" class="max-size"></div>';
    component = getComponent();
    tree = component.toJSON();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });

  describe('useEffect', () => {
    test('should calls getMapId with correct params', async () => {
      await wait(0);
      expect(getMapId).toBeCalled();
      expect(getMapId).toBeCalledWith(event1.eventSlug, sliderId);
    });

    test('should calls loadMap with correct params', async () => {
      await wait(0);
      expect(loadMap).toBeCalled();
      expect(loadMap).toBeCalledWith(event1.place, 'mapId');
    });

    test('should removes max-size class', async () => {
      await wait(0);
      expect(document.getElementById('mapId').classList).toHaveLength(0);
    });
  });
});
