import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../../components/Hero', () => 'Hero');
jest.mock('../../components/Header', () => 'Header');
jest.mock('../../components/Search', () => 'Search');
jest.mock('../../components/TitleList', () => 'TitleList');

import Search from '../../components/Search';
import TitleList from '../../components/TitleList';

import EventHome from '.';

describe('EventHome', () => {
  let user;
  let tree;
  let props;
  let element;
  let tagSlug;
  let instance;
  let component;
  let tagMessage;
  let background;
  let logoHeader;
  let logoLanding;

  const getComponent = allProps => {
    element = <EventHome {...allProps} />;
    component = renderer.create(element);
    instance = component.root;
    return component;
  };

  beforeEach(() => {
    tagSlug = 'tagSlug';
    background = 'background';
    logoHeader = 'logoHeader';
    logoLanding = 'logoLanding';
    tagMessage = 'eventolMessage';
    user = {
      first_name: 'first_name',
      last_name: 'last_name',
    };
    props = {
      user,
      tagSlug,
      background,
      logoHeader,
      logoLanding,
      tagMessage,
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
          component = getComponent({user, isMobile: false, tagSlug});
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
          component = getComponent({user, isMobile: true, tagSlug});
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
          component = getComponent({isMobile: false, tagSlug});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });

      describe('With custom data', () => {
        beforeEach(() => {
          props = {
            tagSlug,
            tagMessage,
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
          component = getComponent({isMobile: true, tagSlug});
          tree = component.toJSON();
        });

        test('Snapshot', () => {
          expect(tree).toMatchSnapshot();
        });
      });

      describe('With custom data', () => {
        beforeEach(() => {
          props = {
            tagSlug,
            tagMessage,
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
