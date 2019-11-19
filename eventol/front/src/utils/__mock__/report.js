const getConfirmationReport = (confirmed, notConfirmed) => ({
  confirmed,
  not_confirmed: notConfirmed,
  total: confirmed + notConfirmed,
});

export const usersReports = {
  attendee: {
    with_event_user: getConfirmationReport(1, 2),
    without_event_user: getConfirmationReport(2, 3),
  },
  collaborator: getConfirmationReport(3, 4),
  event_user: getConfirmationReport(4, 5),
  installer: getConfirmationReport(6, 7),
  organizer: getConfirmationReport(7, 8),
  speakers: 9,
};

export const activitiesReport = {
  level_count: {
    '1': 3,
    '2': 2,
    '3': 1,
  },
  status_count: {
    '1': 2,
    '2': 1,
  },
  type_count: {
    Talk: 4,
    Workshop: 2,
  },
  ...getConfirmationReport(1, 2),
};

export const installationsReport = {
  hardware_count: {
    notebook: 1,
    phone: 2,
  },
  software_count: {
    ubuntu: 3,
    fedora: 2,
    arch: 1,
  },
  installer_count: {
    '1': 2,
    '2': 1,
  },
  total: 2,
};

export const eventReport = {
  // users data
  ...usersReports,

  // activities data
  activity: activitiesReport,

  // installations data
  installation: installationsReport,
};

export const event1PrivateData = {
  id: 1,
  email: 'organizer1@mailinator.com',
  organizers: 'FirstName1 LastName1 Username1',
};

export const event2PrivateData = {
  id: 2,
  email: 'organizer2@mailinator.com',
  organizers: 'FirstName2 LastName2 Username2',
};

export const eventsPrivateData = [
  {...event1PrivateData},
  {...event2PrivateData},
];

export const getEventData = (id, name, tags, report, eventSlug, location) => ({
  id,
  name,
  tags,
  report,
  location,
  event_slug: eventSlug,
});

export const event1Data = getEventData(
  1,
  'event name',
  {name: 'tag name', slug: 'tag slug'},
  eventReport,
  'event_slug',
  ['Capital Federal', 'Pompeya', 'Buenos Aires', 'Argentina']
);

export const event2Data = getEventData(
  2,
  'event 2 name',
  {name: 'tag 2 name', slug: 'tag 2 slug'},
  eventReport,
  'event_2_slug',
  ['Capital Federal', 'Monserrat', 'Buenos Aires', 'Argentina']
);

export const eventsData = [{...event1Data}, {...event2Data}];

export const expectedActivityDetail = {
  levels: {'1': 6, '2': 4, '3': 2},
  status: {'1': 4, '2': 2},
  types: {Talk: 8, Workshop: 4},
};

export const expectedInstallationsSoftwares = {arch: 2, fedora: 4, ubuntu: 6};

export const expectedTotals = {
  activities: {
    confirmed: 2,
    details: expectedActivityDetail,
    not_confirmed: 4,
    total: 6,
  },
  attendees: {confirmed: 6, not_confirmed: 10, total: 16},
  collaborators: {confirmed: 6, not_confirmed: 8, total: 14},
  installations: {softwares: expectedInstallationsSoftwares, total: 4},
  installers: {confirmed: 12, not_confirmed: 14, total: 26},
  organizers: {confirmed: 14, not_confirmed: 16, total: 30},
  speakers: 18,
};

export const expectedEventDataWithoutPrivateData = {
  ...event1Data,
  assistanceDetail: {attendees: {confirmed: 3, not_confirmed: 5, total: 8}},
  locationDetail: {
    address: 'Pompeya',
    address_detail: 'Capital Federal',
    province: 'Buenos Aires',
  },
};

export const expectedEventDataWithPrivateData = {
  ...expectedEventDataWithoutPrivateData,
  ...event1PrivateData,
};

export const expectedValues = {
  expectedTotals,
  expectedActivityDetail,
  expectedInstallationsSoftwares,
  expectedEventDataWithPrivateData,
  expectedEventDataWithoutPrivateData,
};

const mockedData = {
  activitiesReport,
  eventData: event1Data,
  event1Data,
  event2Data,
  eventsData,
  eventReport,
  event1PrivateData,
  event2PrivateData,
  eventsPrivateData,
  getEventData,
  installationsReport,
  usersReports,
  expectedValues,
};
export default mockedData;
