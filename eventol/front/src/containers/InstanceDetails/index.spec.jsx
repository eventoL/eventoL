import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('../../components/Hero', () => 'Hero');
jest.mock('../../components/Header', () => 'Header');
jest.mock('../../components/Search', () => 'Search');
jest.mock('../../components/TitleList', () => 'TitleList');

import Header from '../../components/Header';

import InstanceDetails from '.';

describe('InstanceDetails', () => {
  let background;
  let component;
  let element;
  let eventolMessage;
  let events;
  let instance;
  let isMobile;
  let languages;
  let logoHeader;
  let logoLanding;
  let props;
  let tree;
  let user;
  let users;
  let versions;
  const handleOnChangeLanguage = jest.fn();

  const getComponent = allProps => {
    element = <InstanceDetails {...allProps} />;
    component = renderer.create(element);
    instance = component.root;
    return component;
  };

  beforeEach(() => {
    isMobile = false;
    background = 'background';
    logoHeader = 'logoHeader';
    logoLanding = 'logoLanding';
    events = 500;
    eventolMessage = 'eventolMessage';
    user = {
      first_name: 'first_name',
      last_name: 'last_name',
    };
    languages = [
      {code: 'es', name: 'Spanish'},
      {code: 'en', name: 'English'},
    ];
    users = 4000;
    versions = {
      commit: '3af85e99036166d1267c3794e333a5b12c729561 Fix react lints',
      django: '1.11.29',
      python: '3.9.6 (default, Jun 29 2021, 19:45:46) [GCC 10.2.1 20201203]',
      tag: 'v2.3.0',
    };

    props = {
      background,
      eventolMessage,
      events,
      handleOnChangeLanguage,
      isMobile,
      logoHeader,
      logoLanding,
      user,
      users,
      versions,
    };
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('handlerOnChangeLanguage', () => {
    beforeEach(() => {
      component = getComponent({
        ...props,
        isMobile: false,
        languages,
        handleOnChangeLanguage,
      });
      tree = component.toJSON();
    });

    test('should calls handleOnChangeLanguage with language code when this function exists', async () => {
      const HeaderInstance = instance.findByType(Header);
      HeaderInstance.props.handlerOnChangeLanguage('es');

      expect(handleOnChangeLanguage).toBeCalled();
      expect(handleOnChangeLanguage).toBeCalledWith('es');
    });

    test('should not calls handleOnChangeLanguage when this function not exists', async () => {
      component = getComponent({
        ...props,
        handleOnChangeLanguage: null,
        isMobile: false,
        languages,
      });

      const HeaderInstance = instance.findByType(Header);
      HeaderInstance.props.handlerOnChangeLanguage('es');

      expect(handleOnChangeLanguage).not.toBeCalled();
    });
  });

  describe('With languages', () => {
    test('Snapshot', () => {
      component = getComponent({
        ...props,
        isMobile: false,
        languages,
      });
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });
  });

  describe('With user', () => {
    describe('Desktop', () => {
      beforeEach(() => {
        component = getComponent({...props, user, isMobile: false});
        tree = component.toJSON();
      });

      test('Snapshot', () => {
        expect(tree).toMatchSnapshot();
      });
    });

    describe('Mobile', () => {
      beforeEach(() => {
        component = getComponent({...props, user, isMobile: true});
        tree = component.toJSON();
      });

      test('Snapshot', () => {
        expect(tree).toMatchSnapshot();
      });
    });
  });

  describe('Without user', () => {
    describe('Desktop', () => {
      beforeEach(() => {
        component = getComponent({...props, isMobile: false});
        tree = component.toJSON();
      });

      test('Snapshot', () => {
        expect(tree).toMatchSnapshot();
      });
    });

    describe('Mobile', () => {
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
