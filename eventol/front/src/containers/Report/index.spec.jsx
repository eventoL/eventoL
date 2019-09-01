import wait from 'waait';
import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('react-input-toggle', () => 'Toggle');

jest.mock('../../components/Title', () => 'Title');
jest.mock('../../components/Button', () => 'Button');
jest.mock('../../components/ReportTable', () => 'TableReport');
jest.mock('../../components/ExportButton', () => 'ExportButton');

import Report from '.';
import {eventsPrivateData} from '../../utils/__mock__/report';

describe('Report', () => {
  let tree;
  let element;
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
  });
});
