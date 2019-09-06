import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../ItemMap', () => 'ItemMap');

jest.mock('../../utils/urls', () => ({
  getTagUrl: jest.fn().mockImplementation(() => 'tag-url'),
  goToUrl: jest.fn(),
}));

import ItemMap from '../ItemMap';

import {goToUrl} from '../../utils/urls';
import {event1} from '../../utils/__mock__/data';

import Item from '.';

describe('Item', () => {
  let tree;
  let data;
  let instance;
  let sliderId;
  let component;

  const renderItem = () => {
    component = renderer.create(<Item data={data} sliderId={sliderId} />);
    tree = component.toJSON();
    instance = component.root;
  };

  beforeEach(() => {
    data = undefined;
    sliderId = event1.id;
  });

  afterEach(() => {
    goToUrl.mockClear();
  });

  test('Default render', () => {
    renderItem();
    expect(tree).toMatchSnapshot();
  });

  test('should call goToUrl on click event', () => {
    data = event1;
    renderItem();

    expect(goToUrl).not.toBeCalled();

    instance.children[0].props.children.props.onClick();

    expect(goToUrl).toBeCalled();
    expect(goToUrl).toBeCalledWith(data.url);
  });

  test('should call goToUrl on key press event', () => {
    data = event1;
    renderItem();

    expect(goToUrl).not.toBeCalled();

    instance.children[0].props.children.props.onKeyPress();

    expect(goToUrl).toBeCalled();
    expect(goToUrl).toBeCalledWith(data.url);
  });

  test('should shows ItemMap when data has not backdrop', () => {
    data = {...event1, backdrop: undefined};
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
    renderItem();
    expect(tree).toMatchSnapshot();
  });
});
