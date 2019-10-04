import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../../components/Hero', () => 'Hero');
jest.mock('../../components/Header', () => 'Header');
jest.mock('../../components/Search', () => 'Search');
jest.mock('../../components/TitleList', () => 'TitleList');

import Search from '../../components/Search';
import TitleList from '../../components/TitleList';

import Home from '.';

describe('Home', () => {
  let tree;
  let user;
  let props;
  let element;
  let instance;
  let component;
  let background;
  let logoHeader;
  let logoLanding;
  let eventolMessage;

  const getComponent = allProps => {
    element = <Home {...allProps} />;
    component = renderer.create(element);
    instance = component.root;
    return component;
  };

  beforeEach(() => {
    background = 'background';
    logoHeader = 'logoHeader';
    logoLanding = 'logoLanding';
    eventolMessage = 'eventolMessage';
    user = {
      first_name: 'first_name',
      last_name: 'last_name',
    };
    props = {
      user,
      background,
      logoHeader,
      logoLanding,
      eventolMessage,
    };
  });

  describe('Search', () => {
    beforeEach(() => {
      component = getComponent({});
      tree = component.toJSON();
    });

    test('Should show a new TitleList for search', async () => {
      expect(tree).toMatchSnapshot();

      const value = 'searchTerm';
      instance.findByType(Search).props.onEnter(value);
      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      const titleLists = instance.findAllByType(TitleList);
      expect(titleLists[0].props.id).toEqual('search_results');
    });

    test('Should not show a new TitleList for search with value is ""', async () => {
      expect(tree).toMatchSnapshot();

      const value = '';
      instance.findByType(Search).props.onEnter(value);
      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      const titleLists = instance.findAllByType(TitleList);
      expect(titleLists[0].props.id).not.toEqual('search_results');
    });
  });

  describe('With user', () => {
    describe('Desktop', () => {
      describe('Default', () => {
        beforeEach(() => {
          component = getComponent({user, isMobile: false});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });

      describe('With custom data', () => {
        beforeEach(() => {
          component = getComponent({...props, isMobile: false});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });
    });

    describe('Mobile', () => {
      describe('Default', () => {
        beforeEach(() => {
          component = getComponent({user, isMobile: true});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });

      describe('With custom data', () => {
        beforeEach(() => {
          component = getComponent({...props, isMobile: true});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });
    });
  });

  describe('Without user', () => {
    describe('Desktop', () => {
      describe('Default', () => {
        beforeEach(() => {
          component = getComponent({isMobile: false});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });

      describe('With custom data', () => {
        beforeEach(() => {
          props = {
            eventolMessage,
            background,
            logoHeader,
            logoLanding,
          };
          component = getComponent({...props, isMobile: false});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });
    });

    describe('Mobile', () => {
      describe('Default', () => {
        beforeEach(() => {
          component = getComponent({isMobile: true});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });

      describe('With custom data', () => {
        beforeEach(() => {
          props = {
            eventolMessage,
            background,
            logoHeader,
            logoLanding,
          };
          component = getComponent({...props, isMobile: true});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });
    });
  });
});
