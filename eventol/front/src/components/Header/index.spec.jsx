import React from 'react';
import renderer from 'react-test-renderer';

import Header from '.';

describe('Header', () => {
  let component, tree, user, logo, isMobile;

  beforeEach(() => {
    /* eslint-disable camelcase */
    user = {
      first_name: 'first_name',
      last_name: 'last_name',
    };
    /* eslint-enable camelcase */
    logo = 'eventol.png';
  });

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
