import React from 'react';
import renderer from 'react-test-renderer';

import EventHome from '.';

describe('EventHome', () => {
  let component, tree, background,
    logoHeader, logoLanding, tagMessage,
    tagSlug, user;

  beforeEach(() => {
    background = '';
    logoHeader = '';
    logoLanding = '';
    tagMessage = '';
    tagSlug = '';
    user = {};
    component = renderer.create(
      <EventHome
        background={background}
        logoHeader={logoHeader}
        logoLanding={logoLanding}
        tagMessage={tagMessage}
        tagSlug={tagSlug}
        user={user}
      />,
    );
    tree = component.toJSON();
  });

  test('Snapshot', () => {
    expect(tree).toMatchSnapshot();
  });
});
