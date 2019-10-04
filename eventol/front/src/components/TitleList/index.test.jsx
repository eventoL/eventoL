import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../SliderItems', () => 'SliderItems');
jest.mock('../../utils/urls', () => ({
  getApiFullUrl: jest.fn(() => 'apiFullUrl'),
}));
jest.mock('../../utils/api', () => ({
  getUrl: jest.fn(),
}));
jest.mock('../../utils/events', () => ({
  parseEventToItem: jest.fn(event => event),
  emptyEventItem: {id: 'empty'},
}));

import TitleList from '.';
import {getUrl} from '../../utils/api';
import {events} from '../../utils/__mock__/data';

describe('TitleList', () => {
  let id;
  let url;
  let tree;
  let title;
  let element;
  let showEmpty;
  let component;

  const getComponent = () => {
    element = (
      <TitleList id={id} showEmpty={showEmpty} title={title} url={url} />
    );
    component = renderer.create(element);
    return component;
  };

  beforeEach(() => {
    id = 'id';
    title = 'title';
    url = 'http://url/';
    showEmpty = undefined;
    getUrl.mockImplementationOnce(() => {
      return new Promise(resolve => resolve({results: events}));
    });
    component = getComponent();
    tree = component.toJSON();
  });

  describe('Default with event data in request', () => {
    test('should be null in first render when showEmpty is false', async () => {
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });

    test('should be show empty event in first render when showEmpty is true', async () => {
      showEmpty = true;
      getUrl.mockImplementationOnce(() => {
        return new Promise(resolve => resolve({results: events}));
      });
      component = getComponent();
      tree = component.toJSON();

      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });
  });

  describe('Default without event data in request', () => {
    beforeEach(() => {
      getUrl.mockImplementationOnce(() => {
        return new Promise(resolve => resolve({results: []}));
      });
      component = getComponent();
      tree = component.toJSON();
    });

    test('should be null when showEmpty is false', async () => {
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });

    test('should be show empty event when showEmpty is true', async () => {
      showEmpty = true;
      getUrl.mockImplementationOnce(() => {
        return new Promise(resolve => resolve({results: []}));
      });
      component = getComponent();
      tree = component.toJSON();

      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });
  });
});
