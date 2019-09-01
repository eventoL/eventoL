import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

import Search from '.';

describe('Search', () => {
  let tree;
  let onEnter;
  let element;
  let onChange;
  let instance;
  let component;

  const getComponent = () => {
    element = <Search onChange={onChange} onEnter={onEnter} />;
    component = renderer.create(element);
    return component;
  };

  beforeEach(() => {
    onChange = jest.fn();
    onEnter = jest.fn();
    component = getComponent();
    instance = component.root;
    tree = component.toJSON();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });

    test('Snapshot with update text', async () => {
      expect(tree).toMatchSnapshot();

      const value = 'searchTerm';
      instance.findByType('input').props.onChange({target: {value}});
      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
      expect(instance.findByType('input').props.value).toEqual(value);
    });
  });

  test('handle onChange', () => {
    const value = 'searchTerm';
    instance.findByType('input').props.onChange({target: {value}});
    expect(onChange).toBeCalled();
    expect(onChange).toBeCalledWith(value);
  });

  describe('handle onKeyUp', () => {
    test('With not Enter key', () => {
      instance.findByType('input').props.onKeyUp({key: 'A'});
      expect(onEnter).not.toBeCalled();
    });

    test('With Enter key', () => {
      instance.findByType('input').props.onKeyUp({key: 'Enter'});
      expect(onEnter).toBeCalled();
    });
  });
});
