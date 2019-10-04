import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../Logo', () => 'Logo');
jest.mock('../Navigation', () => 'Navigation');
jest.mock('../UserProfile', () => 'UserProfile');
jest.mock('../SignIn', () => 'SignIn');

import Header from '.';

describe('Header', () => {
  let component;
  let tree;
  let user;
  let logo;
  let event;
  let instance;
  let isMobile;

  beforeEach(() => {
    event = {
      preventDefault: jest.fn(),
      stopPropagation: jest.fn(),
    };
    user = {
      first_name: 'first_name',
      last_name: 'last_name',
    };
    logo = 'eventol.png';
  });

  describe('Default', () => {
    beforeEach(() => {
      document.body.innerHTML =
        '<div><div class="narrow-links" style="display: block"></div></div>';
      component = renderer.create(
        <Header isMobile logoHeader={logo} user={user} />
      );
      tree = component.toJSON();
      instance = component.root;
    });

    test('should call event.stopPropagation and event.preventDefault on click event', () => {
      expect(event.preventDefault).not.toBeCalled();
      expect(event.stopPropagation).not.toBeCalled();

      instance.findByType('button').props.onClick(event);

      expect(event.preventDefault).toBeCalled();
      expect(event.stopPropagation).toBeCalled();
    });

    test('should call event.stopPropagation and event.preventDefault on key press event', () => {
      expect(event.preventDefault).not.toBeCalled();
      expect(event.stopPropagation).not.toBeCalled();

      instance.findByType('button').props.onKeyPress(event);

      expect(event.preventDefault).toBeCalled();
      expect(event.stopPropagation).toBeCalled();
    });

    test('should change display of narrow-links', () => {
      expect(event.preventDefault).not.toBeCalled();
      expect(event.stopPropagation).not.toBeCalled();

      instance.findByType('button').props.onClick(event);

      let linksEl = document.querySelector('.narrow-links');
      expect(linksEl.style.display).toEqual('none');

      instance.findByType('button').props.onKeyPress(event);

      linksEl = document.querySelector('.narrow-links');
      expect(linksEl.style.display).toEqual('block');
    });
  });

  describe('With user', () => {
    describe('Mobile version', () => {
      beforeEach(() => {
        isMobile = true;
        component = renderer.create(
          <Header isMobile={isMobile} logoHeader={logo} user={user} />
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
          <Header isMobile={isMobile} logoHeader={logo} user={user} />
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
        component = renderer.create(<Header isMobile={isMobile} />);
        tree = component.toJSON();
      });

      test('Snapshot', () => {
        expect(tree).toMatchSnapshot();
      });
    });

    describe('Desktop version', () => {
      beforeEach(() => {
        isMobile = false;
        component = renderer.create(<Header isMobile={isMobile} />);
        tree = component.toJSON();
      });

      test('Snapshot', () => {
        expect(tree).toMatchSnapshot();
      });
    });
  });
});
