import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('react-input-toggle', () => 'Toggle');

jest.mock('../../components/Title', () => 'Title');
jest.mock('../../components/Button', () => 'Button');
jest.mock('../../components/ReportTable', () => 'ReportTable');
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
import ReportTable from '../../components/ReportTable';
import {loadReports} from '../../utils/api';
import {events} from '../../utils/__mock__/data';
import {parseTotals, parseEvent} from '../../utils/report';
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

      expect(instance.findByType(Toggle).props.checked).toBeTruthy();

      instance.findByType(Toggle).props.onChange();
      component.update(element);
      await wait(0);

      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      instance = component.root;
      expect(instance.findByType(Toggle).props.checked).toBeFalsy();
    });
  });

  describe('Snapshots', () => {
    beforeEach(() => {
      loadReports.mockImplementationOnce(() => {
        return new Promise(resolve =>
          resolve({count: events.length, results: events})
        );
      });
    });

    test('Default', async () => {
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();

      expect(tree).toMatchSnapshot();
    });

    test('loadReports', async () => {
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();

      expect(tree).toMatchSnapshot();
    });

    test('fetchData', async () => {
      parseEvent.mockReturnValue('parseEventObject');
      parseTotals.mockReturnValue('parseTotalsObject');

      const reportTableInstance = instance.findByType(ReportTable);

      expect(reportTableInstance).toBeDefined();
      expect(tree).toMatchSnapshot();

      const {fetchData} = reportTableInstance.props;
      fetchData({
        pageSize: 15,
        page: 0,
        sorted: {desc: false, id: 'name'},
        filtered: [],
      });

      component.update(element);
      await wait(0);
      tree = component.toJSON();

      expect(tree).toMatchSnapshot();
    });
  });
});
