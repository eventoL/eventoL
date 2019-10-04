import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('react-csv', () => ({CSVLink: 'CSVLink'}));

import ExportButton from '.';
import {eventsData} from '../../utils/__mock__/report';

describe('ExportButton', () => {
  let tree;
  let element;
  let columns;
  let instance;
  let component;

  beforeEach(() => {
    columns = [
      {
        Header: 'Event',
        columns: [
          {
            Footer: 'Footer',
            Header: 'Name',
            accessor: 'name',
            minWidth: 150,
            resizable: false,
            sortable: true,
            total: 'Events: 1',
          },
        ],
      },
      {columns: []},
      {
        Footer: 'Footer id',
        Header: 'ID',
        accessor: 'id',
        minWidth: 150,
        resizable: false,
        sortable: true,
        total: 'Ids: 1',
      },
      {
        Header: 'Tag',
        columns: [
          {
            Footer: 'Footer 2',
            Header: 'Tag',
            accessor: ({tags: {name}}) => name,
            minWidth: 200,
            resizable: false,
            sortable: true,
            total: 'Tags: 1',
          },
          {
            Footer: 'Footer 3',
            Header: 'Slug',
            accessor: ({tags: {slug}}) => slug,
            minWidth: 100,
            resizable: false,
            sortable: true,
            total: 'Slugs: 1',
          },
        ],
      },
    ];
  });

  describe('Without data', () => {
    beforeEach(() => {
      element = (
        <ExportButton
          data={[]}
          filename="export"
          label="Label"
          type="default"
        />
      );
      component = renderer.create(element);
      tree = component.toJSON();
      instance = component.getInstance();
    });

    test('Default', async () => {
      expect(tree).toMatchSnapshot();

      expect(instance.state.header).toEqual([]);
      expect(instance.state.rows).toEqual([]);
      expect(instance.state.totals).toEqual([]);

      instance.updateCsv(columns);

      component.update(element);
      await wait(0);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      expect(instance.state.header).toEqual([]);
      expect(instance.state.rows).toEqual([]);
      expect(instance.state.totals).toEqual([]);
    });
  });

  describe('With data', () => {
    beforeEach(() => {
      element = (
        <ExportButton
          data={eventsData}
          filename="export"
          label="Label"
          type="default"
        />
      );
      component = renderer.create(element);
      tree = component.toJSON();
      instance = component.getInstance();
    });

    test('Default', async () => {
      expect(tree).toMatchSnapshot();

      expect(instance.state.header).toEqual([]);
      expect(instance.state.rows).toEqual([]);
      expect(instance.state.totals).toEqual([]);

      instance.updateCsv(columns);

      component.update(element);
      await wait(0);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      expect(instance.state.header).toEqual(['Name', 'ID', 'Tag', 'Slug']);
      expect(instance.state.rows).toEqual([
        ['event name', 1, 'tag name', 'tag slug'],
        ['event 2 name', 2, 'tag 2 name', 'tag 2 slug'],
      ]);
      expect(instance.state.totals).toEqual([
        'Events: 1',
        'Ids: 1',
        'Tags: 1',
        'Slugs: 1',
      ]);
    });
  });
});
