jest.mock('react-sizes', () => () => Component => props => <Component {...props} />);

jest.mock('../../components/Hero', () => 'Hero');
jest.mock('../../components/Header', () => 'Header');
jest.mock('../../components/Search', () => 'Search');
jest.mock('../../components/TitleList', () => 'TitleList');

import React from 'react';
import renderer from 'react-test-renderer';

import EventHome from '.';


describe('EventHome', () => {
  let component, tree, background,
    logoHeader, logoLanding, tagSlug,
    tagMessage, user, props;

  const getComponent = allProps => {
    component = renderer.create(<EventHome {...allProps} />);
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
