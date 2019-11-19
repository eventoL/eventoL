import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../Logo', () => 'Logo');
jest.mock('../Navigation', () => 'Navigation');
jest.mock('../UserProfile', () => 'UserProfile');
jest.mock('../SignIn', () => 'SignIn');

import Header from '.';

describe('Header', () => {
  let component, tree, user, logo, isMobile;

  beforeEach(() => {
    user = {
      first_name: 'first_name',
      last_name: 'last_name',
    };
    logo = 'eventol.png';
  });

  describe('With user', () => {
    describe('Mobile version', () => {
      beforeEach(() => {
        isMobile = true;
        component = renderer.create(
          <Header logoHeader={logo} user={user} isMobile={isMobile} />,
        );
        tree = component.toJSON();
      });

      test('Snapshot', () => {
        expect(tree).toMatchSnapshot();
      });
    });

    describe('Desktop version', () => {
      beforeEach(() => {
        isMobile = false;
        component = renderer.create(
          <Header logoHeader={logo} user={user} isMobile={isMobile} />,
        );
        tree = component.toJSON();
      });

      test('Snapshot', () => {
        expect(tree).toMatchSnapshot();
      });
    });
  });

  describe('Without user and without logo', () => {
    describe('Mobile version', () => {
      beforeEach(() => {
        isMobile = true;
        component = renderer.create(
          <Header isMobile={isMobile} />,
        );
        tree = component.toJSON();
      });

      test('Snapshot', () => {
        expect(tree).toMatchSnapshot();
      });
    });

    describe('Desktop version', () => {
      beforeEach(() => {
        isMobile = false;
        component = renderer.create(
          <Header isMobile={isMobile} />,
        );
        tree = component.toJSON();
      });

      test('Snapshot', () => {
        expect(tree).toMatchSnapshot();
      });
    });
  });
});
