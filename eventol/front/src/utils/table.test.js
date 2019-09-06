import {getColumns} from './table';

import {eventsPrivateData, expectedTotals} from './__mock__/report';

describe('Table utils', () => {
  const validateHeaders = (data, headers) => {
    expect(data).toHaveLength(headers.length);
    headers.forEach(({name, columns}, index) => {
      expect(data[index]).toHaveProperty('Header', name);
      if (columns.length > 0) {
        expect(data[index].columns).toHaveLength(columns.length);
        columns.forEach((columnName, columnIndex) => {
          expect(data[index].columns[columnIndex]).toHaveProperty(
            'Header',
            columnName
          );
        });
      }
    });
  };

  const confirmationColumns = ['Confirmed', 'Not Confirmed', 'Total'];

  describe('getColumns', () => {
    test('default', () => {
      const data = getColumns(
        '',
        eventsPrivateData,
        eventsPrivateData.length,
        expectedTotals
      );

      validateHeaders(data, [
        {name: 'Event', columns: ['Name']},
        {name: 'Location', columns: ['Address detail', 'Address', 'Province']},
        {name: 'Organizers', columns: ['Email', 'Organizers']},
      ]);

      expect(data[0].columns[0]).toHaveProperty('Footer');
      expect(data[0].columns[0].accessor).toEqual('name');
      expect(data[0].columns[0].minWidth).toEqual(150);
      expect(data[0].columns[0].resizable).toEqual(false);
      expect(data[0].columns[0].sortable).toEqual(true);
      expect(data[0].columns[0].total).toEqual('Events: 2');
    });

    test('confirmed', () => {
      const data = getColumns(
        'confirmed',
        eventsPrivateData,
        eventsPrivateData.length,
        expectedTotals
      );

      validateHeaders(data, [
        {name: 'Event', columns: ['Name']},
        {name: 'Location', columns: ['Address detail', 'Address', 'Province']},
        {name: 'Organizers', columns: ['Email', 'Organizers']},
        {
          name: 'Assistance (confirmed)',
          columns: [
            'Attendees',
            'Organizers',
            'Collaborators',
            'Installers',
            'Speakers',
          ],
        },
        {name: 'Activities', columns: ['Activities', 'Installations']},
      ]);

      expect(data[0].columns[0]).toHaveProperty('Footer');
      expect(data[0].columns[0].accessor).toEqual('name');
      expect(data[0].columns[0].minWidth).toEqual(150);
      expect(data[0].columns[0].resizable).toEqual(false);
      expect(data[0].columns[0].sortable).toEqual(true);
      expect(data[0].columns[0].total).toEqual('Events: 2');
    });

    test('installations', () => {
      const data = getColumns(
        'installations',
        eventsPrivateData,
        eventsPrivateData.length,
        expectedTotals
      );

      validateHeaders(data, [
        {name: 'Event', columns: ['Name']},
        {name: 'Location', columns: ['Address detail', 'Address', 'Province']},
        {name: 'Organizers', columns: ['Email', 'Organizers']},
        {name: 'Installers', columns: confirmationColumns},
        {
          name: 'Installations',
          columns: ['Quantity', 'arch', 'fedora', 'ubuntu'],
        },
      ]);

      expect(data[0].columns[0]).toHaveProperty('Footer');
      expect(data[0].columns[0].accessor).toEqual('name');
      expect(data[0].columns[0].minWidth).toEqual(150);
      expect(data[0].columns[0].resizable).toEqual(false);
      expect(data[0].columns[0].sortable).toEqual(true);
      expect(data[0].columns[0].total).toEqual('Events: 2');
    });

    test('assitance', () => {
      const data = getColumns(
        'assitance',
        eventsPrivateData,
        eventsPrivateData.length,
        expectedTotals
      );

      validateHeaders(data, [
        {name: 'Event', columns: ['Name']},
        {name: 'Location', columns: ['Address detail', 'Address', 'Province']},
        {name: 'Organizers', columns: ['Email', 'Organizers']},
        {name: 'Attendees', columns: confirmationColumns},
        {name: 'Collaborators', columns: confirmationColumns},
        {name: 'Installers', columns: confirmationColumns},
        {name: 'Organizers', columns: confirmationColumns},
        {name: 'Speakers', columns: []},
      ]);

      expect(data[0].columns[0]).toHaveProperty('Footer');
      expect(data[0].columns[0].accessor).toEqual('name');
      expect(data[0].columns[0].minWidth).toEqual(150);
      expect(data[0].columns[0].resizable).toEqual(false);
      expect(data[0].columns[0].sortable).toEqual(true);
      expect(data[0].columns[0].total).toEqual('Events: 2');
    });

    test('activities', () => {
      const data = getColumns(
        'activities',
        eventsPrivateData,
        eventsPrivateData.length,
        expectedTotals
      );

      validateHeaders(data, [
        {name: 'Event', columns: ['Name']},
        {name: 'Location', columns: ['Address detail', 'Address', 'Province']},
        {name: 'Organizers', columns: ['Email', 'Organizers']},
        {name: 'Speakers', columns: []},
        {
          name: 'Attendees',
          columns: [
            ...confirmationColumns,
            'Proposal',
            'Accepted',
            undefined,
            undefined,
            'Beginner',
            'Medium',
            'Advanced',
          ],
        },
      ]);
      expect(data[0].columns[0]).toHaveProperty('Footer');
      expect(data[0].columns[0].accessor).toEqual('name');
      expect(data[0].columns[0].minWidth).toEqual(150);
      expect(data[0].columns[0].resizable).toEqual(false);
      expect(data[0].columns[0].sortable).toEqual(true);
      expect(data[0].columns[0].total).toEqual('Events: 2');
    });
  });
});
