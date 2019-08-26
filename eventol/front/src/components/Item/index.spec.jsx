import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../ItemMap', () => 'ItemMap');

jest.mock('../../utils/urls', () => ({
  getTagUrl: jest.fn().mockImplementation(() => 'tag-url'),
  goToUrl: jest.fn(),
}));

import ItemMap from '../ItemMap';

import {event1} from '../../utils/__mock__/data';
import {getTagUrl, goToUrl} from '../../utils/urls';

import Item from '.';

describe('Item', () => {
  let component;
  let tree;
  let data;
  let sliderId;

  const renderItem = () => {
    component = renderer.create(<Item data={data} sliderId={sliderId} />);
    tree = component.toJSON();
  };

  beforeEach(() => {
    data = undefined;
    sliderId = undefined;
  });

  test('Default render', () => {
    renderItem();
    expect(tree).toMatchSnapshot();
  });

  test('should shows ItemMap when data has not backdrop', () => {
    data = {backdrop: undefined};
    renderItem();
    expect(tree).toMatchSnapshot();

    const itemMap = component.root.findByType(ItemMap);
    expect(itemMap).toBeDefined();

    expect(itemMap.props.sliderId).toEqual(sliderId);
    const props = [
      'attendees',
      'eventSlug',
      'overview',
      'place',
      'title',
      'url',
    ];
    props.forEach(prop => expect(itemMap.props[prop]).toEqual(data[prop]));
  });

  test('Render event 1', () => {
    data = event1;
    sliderId = event1.id;
    renderItem();
    expect(tree).toMatchSnapshot();
  });
});
