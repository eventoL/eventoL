import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../../utils/events', () => ({
  getSlugParsed: jest.fn().mockImplementation(() => 'parsed-slug'),
}));

jest.mock('../../utils/constants', () => ({
  BACKGROUND_DEFAULT: 'BACKGROUND_DEFAULT',
  LOGO_LANDING_DEFAULT: 'LOGO_LANDING_DEFAULT',
}));

jest.mock('../../utils/urls', () => ({
  CREATE_EVENT: 'CREATE_EVENT',
}));

import {getSlugParsed} from '../../utils/events';

import Hero from '.';

describe('Hero', () => {
  let component;
  let tree;
  let background;
  let logoLanding;
  let message;
  let slug;
  let isLogged;

  const renderHero = () => {
    component = renderer.create(
      <Hero
        background={background}
        isLogged={isLogged}
        logoLanding={logoLanding}
        message={message}
        slug={slug}
      />
    );
    tree = component.toJSON();
  };

  beforeEach(() => {
    background = undefined;
    logoLanding = undefined;
    message = undefined;
    slug = undefined;
    isLogged = undefined;
  });

  test('Default render', () => {
    renderHero();
    expect(tree).toMatchSnapshot();
  });

  test('With message', () => {
    message = 'message';
    renderHero();
    expect(tree).toMatchSnapshot();
  });

  test('With slug', () => {
    slug = 'slug';
    renderHero();

    expect(tree).toMatchSnapshot();
    expect(getSlugParsed).toBeCalled();
    expect(getSlugParsed).toBeCalledWith(slug);
  });

  test('With custom backgound', () => {
    background = 'custom-background';
    renderHero();
    expect(tree).toMatchSnapshot();
  });

  test('With custom logo', () => {
    logoLanding = 'logo-custom';
    renderHero();
    expect(tree).toMatchSnapshot();
  });

  test('With user (isLogged is true)', () => {
    isLogged = true;
    renderHero();
    expect(tree).toMatchSnapshot();
  });
});
