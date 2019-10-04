import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('react-input-toggle', () => 'Toggle');

jest.mock('../../components/Title', () => 'Title');
jest.mock('../../components/Button', () => 'Button');
jest.mock('../../components/ReportTable', () => 'TableReport');
jest.mock('../../components/ExportButton', () => 'ExportButton');

jest.mock('../../utils/logger', () => ({error: jest.fn()}));
jest.mock('../../utils/api', () => ({
  loadReports: jest.fn(),
}));
jest.mock('../../utils/report', () => ({
  parseTotals: jest.fn(),
  parseEvent: jest.fn(),
}));

import Toggle from 'react-input-toggle';
import Report from '.';
import {loadReports} from '../../utils/api';
import {events} from '../../utils/__mock__/data';
import {eventsPrivateData} from '../../utils/__mock__/report';

describe('Report', () => {
  let tree;
  let element;
  let instance;
  let component;
  let communicator;

  beforeEach(() => {
    communicator = {
      addOnMessage: jest.fn(),
    };

    element = (
      <Report
        communicator={communicator}
        eventsPrivateData={eventsPrivateData}
      />
    );
    component = renderer.create(element);
    instance = component.root;
    tree = component.toJSON();
  });

  describe('Toggle update autoupdate on onChange event', () => {
    test('toggle autoupdate value', async () => {
      expect(tree).toMatchSnapshot();

      instance.findByType(Toggle).props.onChange();
      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      expect(component.getInstance().state.autoupdate).toBeTruthy();

      instance.findByType(Toggle).props.onChange();
      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      instance = component.getInstance();
      expect(component.getInstance().state.autoupdate).toBeFalsy();
    });
  });

  describe('Snapshots', () => {
    test('Default', async () => {
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();

      expect(tree).toMatchSnapshot();
    });

    test('fetch data', async () => {
      loadReports.mockImplementationOnce(() => {
        return new Promise(resolve =>
          resolve({count: events.length, results: events})
        );
      });

      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();

      expect(tree).toMatchSnapshot();

      instance = component.getInstance();
      instance.fetchData(5, 1, false, false);

      component.update(element);
      await wait(0);
      tree = component.toJSON();

      expect(tree).toMatchSnapshot();
    });
  });
});
