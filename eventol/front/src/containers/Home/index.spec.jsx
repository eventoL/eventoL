import React from 'react';
import renderer from 'react-test-renderer';

import Home from '.';

describe('EventHome', () => {
  let component, tree, background,
    logoHeader, logoLanding,
    eventolMessage, user;

  beforeEach(() => {
    background = '';
    logoHeader = '';
    logoLanding = '';
    eventolMessage = '';
    user = {};
    component = renderer.create(
      <Home
        background={background}
        logoHeader={logoHeader}
        logoLanding={logoLanding}
        eventolMessage={eventolMessage}
        user={user}
      />,
    );
    tree = component.toJSON();
  });

  test('Snapshot', () => {
    expect(tree).toMatchSnapshot();
  });
});