import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('react-table', () => 'ReactTable');
jest.mock('../ExportButton', () =>
  jest.fn(() => ({
    updateCsv: jest.fn(),
  }))
);
jest.mock('../../utils/table', () => ({
  getColumns: jest.fn(),
}));

import ReportTable from '.';
import ExportButton from '../ExportButton';
import {getColumns} from '../../utils/table';
import {
  eventsData,
  eventsPrivateData,
  expectedTotals,
} from '../../utils/__mock__/report';

describe('Report', () => {
  let tree;
  let table;
  let count;
  let columns;
  let element;
  let exportButton;
  let component;
  let communicator;

  beforeEach(() => {
    count = 0;
    table = 'confirmed';
    columns = 'columns';
    exportButton = new ExportButton();
    getColumns.mockImplementation(() => columns);

    element = (
      <ReportTable
        communicator={communicator}
        count={0}
        data={eventsData}
        defaultRows={15}
        eventsPrivateData={eventsPrivateData}
        exportButton={exportButton}
        fetchData={jest.fn()}
        isLoading
        pages={null}
        table={table}
        totals={expectedTotals}
      />
    );
    component = renderer.create(element);
    tree = component.toJSON();
  });

  describe('Snapshots', () => {
    test('Default', async () => {
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });

    test('should calls getColumns function with correct params', () => {
      expect(getColumns).toBeCalled();
      expect(getColumns).toBeCalledWith(
        table,
        eventsPrivateData,
        count,
        expectedTotals
      );
    });

    test('should calls exportButton.updateCsv function with correct params', () => {
      expect(exportButton.updateCsv).toBeCalled();
      expect(exportButton.updateCsv).toBeCalledWith(columns);
    });
  });
});
