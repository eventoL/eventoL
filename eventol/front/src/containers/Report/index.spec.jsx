import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

// jest.mock('react-input-toggle', () => 'Toggle');

// jest.mock('../../components/Title', () => 'Title');
// jest.mock('../../components/Button', () => 'Button');
// jest.mock('../../components/ReportTable', () => 'TableReport');
// jest.mock('../../components/ExportButton', () => 'ExportButton');

// jest.mock('../../utils/logger', () => ({error: jest.fn()}));

import Report from '.';

describe('Report', () => {
  let tree;
  let element;
  let eventData;
  let component;
  let communicator;

  beforeEach(() => {
    eventData = {
      name: 'Alias cupidie',
      tags: [
        {
          name: 'qwertyui',
          slug: 'qwertyui',
        },
      ],
      report: {
        event_user: {
          total: 4,
          confirmed: 0,
          not_confirmed: 4,
        },
        collaborator: {
          total: 1,
          confirmed: 0,
          not_confirmed: 1,
        },
        organizer: {
          total: 2,
          confirmed: 0,
          not_confirmed: 2,
        },
        attendee: {
          with_event_user: {
            total: 1,
            confirmed: 2,
            not_confirmed: -1,
          },
          without_event_user: {
            total: 5,
            confirmed: 2,
            not_confirmed: 3,
          },
        },
        installer: {
          total: 1,
          confirmed: 0,
          not_confirmed: 1,
        },
        activity: {
          level_count: {
            '2': 2,
            '3': 2,
          },
          status_count: {
            '1': 1,
            '2': 3,
          },
          type_count: {
            Talk: 4,
          },
          confirmed: 3,
          not_confirmed: 1,
          total: 4,
        },
        installation: {
          hardware_count: {
            '1234': 1,
            asd: 1,
          },
          software_count: {
            ubuntu: 1,
            ';laskdas;dlk': 1,
          },
          installer_count: {
            '23': 2,
          },
          total: 2,
        },
        speakers: 3,
      },
      event_slug: 'qwertyui',
      id: 18,
      location: ['San Nicolas', 'Comuna 1', 'Buenos Aires', 'Argentina'],
    };

    communicator = {
      addOnMessage: jest.fn(),
    };

    const allData = {
      report: {
        event_user: {
          total: 4,
          confirmed: 0,
          not_confirmed: 4,
        },
        collaborator: {
          total: 1,
          confirmed: 0,
          not_confirmed: 1,
        },
        organizer: {
          total: 2,
          confirmed: 0,
          not_confirmed: 2,
        },
        attendee: {
          with_event_user: {
            total: 1,
            confirmed: 2,
            not_confirmed: -1,
          },
          without_event_user: {
            total: 5,
            confirmed: 2,
            not_confirmed: 3,
          },
        },
        installer: {
          total: 1,
          confirmed: 0,
          not_confirmed: 1,
        },
        activity: {
          level_count: {
            '2': 2,
            '3': 2,
          },
          status_count: {
            '1': 1,
            '2': 3,
          },
          type_count: {
            Talk: 4,
          },
          confirmed: 3,
          not_confirmed: 1,
          total: 4,
        },
        installation: {
          hardware_count: {
            '1234': 1,
            asd: 1,
          },
          software_count: {
            ubuntu: 1,
            ';laskdas;dlk': 1,
          },
          installer_count: {
            '23': 2,
          },
          total: 2,
        },
        speakers: 3,
      },
    };
    fetch.mockResponseOnce(JSON.stringify({count: 1, results: [eventData]}));
    fetch.mockResponseOnce(JSON.stringify({results: [allData]}));

    element = <Report communicator={communicator} />;
    component = renderer.create(element);
    tree = component.toJSON();
  });

  afterEach(() => {
    fetch.resetMocks();
  });

  describe('Snapshots', () => {
    test('Default', async () => {
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
      component.update(element);
      await wait(0);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();

      component.update(element);
      await wait(0);
      tree = component.toJSON();
      expect(tree).toMatchSnapshot();
    });
  });
});
