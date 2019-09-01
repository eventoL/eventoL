import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../../utils/urls', () => ({
  PROFILE_URL: 'PROFILE_URL',
}));

import UserProfile from '.';

describe('UserProfile', () => {
  let user;
  let tree;
  let component;

  const getComponent = () => {
    component = renderer.create(<UserProfile user={user} />);
    return component;
  };

  beforeEach(() => {
    user = {
      first_name: 'first_name',
      last_name: 'last_name',
    };
    component = getComponent();
    tree = component.toJSON();
  });

  describe('Default', () => {
    test('Snapshot', () => {
      expect(tree).toMatchSnapshot();
    });
  });
});
