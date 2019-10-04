import {
  getColumns,
  getLocationColumns,
  getAssitanceConfirmatedColumns,
  getActivitiesColumns,
  getConfirmationColumnsBy,
  getAssistancesFullColumns,
  getSoftwaresColumns,
  getInstallationsColumns,
  getActivitiesFieldsColumns,
  getActivitiesFullColumns,
} from './table';

import {
  eventsPrivateData,
  expectedTotals,
  expectedEventDataWithPrivateData,
  expectedEventDataWithoutPrivateData,
} from './__mock__/report';

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

  describe('required fields', () => {
    test('getAssitanceConfirmatedColumns', () => {
      const response = getAssitanceConfirmatedColumns({});
      expect(response).toEqual({});
    });

    test('getActivitiesColumns', () => {
      const response = getActivitiesColumns({});
      expect(response).toEqual({});
    });

    test('getConfirmationColumnsBy', () => {
      const category = 'attendees';
      const totalCategory = 'attendees';
      const field = 'assistanceDetail';
      const title = 'Attendees';
      const response = getConfirmationColumnsBy(
        {},
        category,
        totalCategory,
        field,
        title
      );
      expect(response).toEqual({});
    });

    test('getAssistancesFullColumns', () => {
      const response = getAssistancesFullColumns({});
      expect(response).toEqual({});
    });

    test('getSoftwaresColumns', () => {
      const response = getSoftwaresColumns({});
      expect(response).toEqual([]);
    });

    test('getInstallationsColumns', () => {
      const response = getInstallationsColumns({});
      expect(response).toEqual({});
    });

    test('getActivitiesFieldsColumns', () => {
      const response = getActivitiesFieldsColumns({});
      expect(response).toEqual([]);
    });

    test('getActivitiesFullColumns', () => {
      const response = getActivitiesFullColumns({});
      expect(response).toEqual([]);
    });
  });

  describe('accessors', () => {
    test('getLocationColumns', () => {
      const {columns} = getLocationColumns();
      expect(columns[0].accessor(expectedEventDataWithPrivateData)).toEqual(
        expectedEventDataWithPrivateData.locationDetail.address_detail
      );
      expect(columns[1].accessor(expectedEventDataWithPrivateData)).toEqual(
        expectedEventDataWithPrivateData.locationDetail.address
      );
      expect(columns[2].accessor(expectedEventDataWithPrivateData)).toEqual(
        expectedEventDataWithPrivateData.locationDetail.province
      );
    });

    test('getAssitanceConfirmatedColumns', () => {
      const {columns} = getAssitanceConfirmatedColumns(expectedTotals);
      expect(columns[0].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithPrivateData.assistanceDetail.attendees.confirmed
      );
      expect(columns[1].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithPrivateData.report.organizer.confirmed
      );
      expect(columns[2].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithPrivateData.report.collaborator.confirmed
      );
      expect(columns[3].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithPrivateData.report.installer.confirmed
      );
      expect(columns[4].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithPrivateData.report.speakers
      );
    });

    test('getActivitiesColumns', () => {
      const {columns} = getActivitiesColumns(expectedTotals);
      expect(columns[0].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithPrivateData.report.activity.total
      );
      expect(columns[1].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithPrivateData.report.installation.total
      );
    });

    test('getConfirmationColumnsBy', () => {
      const category = 'attendees';
      const totalCategory = 'attendees';
      const field = 'assistanceDetail';
      const title = 'Attendees';
      const {columns} = getConfirmationColumnsBy(
        expectedTotals,
        category,
        totalCategory,
        field,
        title
      );
      expect(columns[0].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithoutPrivateData[field][category].confirmed
      );
      expect(columns[1].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithoutPrivateData[field][category].not_confirmed
      );
      expect(columns[2].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithoutPrivateData[field][category].total
      );
    });

    test('getAssistancesFullColumns', () => {
      const {speakers} = getAssistancesFullColumns(expectedTotals);
      expect(speakers.accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithPrivateData.report.speakers
      );
    });

    test('getSoftwaresColumns', () => {
      const softwareColumns = getSoftwaresColumns(expectedTotals);
      softwareColumns.forEach(softwareColumn => {
        const software = softwareColumn.Header;
        expect(
          softwareColumn.accessor(expectedEventDataWithoutPrivateData)
        ).toEqual(
          expectedEventDataWithPrivateData.report.installation.software_count[
            software
          ]
        );
      });
    });

    test('getInstallationsColumns', () => {
      const {columns} = getInstallationsColumns(expectedTotals);
      expect(columns[0].accessor(expectedEventDataWithoutPrivateData)).toEqual(
        expectedEventDataWithPrivateData.report.installation.total
      );
    });

    test('getActivitiesFieldsColumns', () => {
      const category = 'status';
      const pluralCategory = 'status';
      const names = ['Proposal', 'Accepted', 'Rejected'];
      const columns = getActivitiesFieldsColumns(
        expectedTotals,
        category,
        pluralCategory,
        names
      );
      columns.forEach((column, index) => {
        expect(column.accessor(expectedEventDataWithoutPrivateData)).toEqual(
          expectedEventDataWithPrivateData.report.activity[`${category}_count`][
            `${index + 1}`
          ]
        );
      });
    });
  });
});
