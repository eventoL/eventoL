import {
  parseInstallationSoftwares,
  parseActivitiesDetails,
  parseTotals,
  parseEvent,
} from './report';
import {
  event1Data,
  eventsData,
  expectedValues,
  eventsPrivateData,
  event2PrivateData,
} from './__mock__/report';

describe('Report utils', () => {
  describe('parseInstallationSoftwares', () => {
    test('should returns correct report', () => {
      const installationsSoftwares = parseInstallationSoftwares(eventsData);
      expect(installationsSoftwares).toEqual(
        expectedValues.expectedInstallationsSoftwares
      );
    });
  });

  describe('parseActivitiesDetails', () => {
    test('should returns correct report', () => {
      const activityDetail = parseActivitiesDetails(eventsData);
      expect(activityDetail).toEqual(expectedValues.expectedActivityDetail);
    });
  });

  describe('parseTotals', () => {
    test('should returns correct report', () => {
      const totals = parseTotals(eventsData);
      expect(totals).toEqual(expectedValues.expectedTotals);
    });
  });

  describe('parseEvent', () => {
    test('should returns correct report without private data', () => {
      const eventData = parseEvent(event1Data);
      expect(eventData).toEqual(
        expectedValues.expectedEventDataWithoutPrivateData
      );
    });

    test('should returns correct report without private data of the event', () => {
      const eventData = parseEvent(event1Data, [event2PrivateData]);
      expect(eventData).toEqual(
        expectedValues.expectedEventDataWithoutPrivateData
      );
    });

    test('should returns correct report with private data', () => {
      const eventData = parseEvent(event1Data, eventsPrivateData);
      expect(eventData).toEqual(
        expectedValues.expectedEventDataWithPrivateData
      );
    });
  });
});
