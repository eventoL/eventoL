import React from 'react';
import renderer from 'react-test-renderer';

jest.mock('react-input-toggle', () => 'Toggle');
jest.mock('../../utils/logger', () => 'Logger');
jest.mock('../../components/Title', () => 'Title');
jest.mock('../../components/Button', () => 'Button');
jest.mock('../../components/ReportTable', () => 'TableReport');
jest.mock('../../components/ExportButton', () => 'ExportButton');

import Report from '.';

describe('Report', () => {
  let tree;
  let component;
  let communicator;

  beforeEach(() => {
    communicator = {
      addOnMessage: jest.fn(),
    };
    fetch.mockResponseOnce(JSON.stringify({}));
    component = renderer.create(<Report communicator={communicator} />);
    tree = component.toJSON();
  });

  afterEach(() => {
    fetch.resetMocks();
  });

  describe('Snapshots', () => {
    test('Default', () => {
      expect(tree).toMatchSnapshot();
    });
  });
});
