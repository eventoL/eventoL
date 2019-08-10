import _ from 'lodash';

export const parseInstallationSoftwares = allData => {
  const softwares = new Set();
  allData.forEach(event =>
    Object.keys(event.report.installation.software_count).forEach(key =>
      softwares.add(key)
    )
  );
  const installationsSoftwares = {};
  softwares.forEach(software => {
    const sum = _.sumBy(
      allData,
      `report.installation.software_count.${software}`
    );
    installationsSoftwares[software] = sum;
  });
  return installationsSoftwares;
};

export const parseActivitiesDetails = allData => {
  const status = new Set();
  const types = new Set();
  const levels = new Set();
  allData.forEach(event => {
    Object.keys(event.report.activity.status_count).forEach(key =>
      status.add(key)
    );
    Object.keys(event.report.activity.type_count).forEach(key =>
      types.add(key)
    );
    Object.keys(event.report.activity.level_count).forEach(key =>
      levels.add(key)
    );
  });
  const activityDetail = {types: {}, status: {}, levels: {}};
  status.forEach(element => {
    const sum = _.sumBy(allData, `report.activity.status_count.${element}`);
    activityDetail.status[element] = sum;
  });
  types.forEach(type => {
    const sum = _.sumBy(allData, `report.activity.type_count.${type}`);
    activityDetail.types[type] = sum;
  });
  levels.forEach(level => {
    const sum = _.sumBy(allData, `report.activity.level_count.${level}`);
    activityDetail.levels[level] = sum;
  });
  return activityDetail;
};

export const parseTotals = allData => {
  const totals = {
    speakers: _.sumBy(allData, 'report.speakers'),
    attendees: {
      confirmed:
        _.sumBy(allData, 'report.attendee.with_event_user.confirmed') +
        _.sumBy(allData, 'report.attendee.without_event_user.confirmed'),
      not_confirmed:
        _.sumBy(allData, 'report.attendee.with_event_user.not_confirmed') +
        _.sumBy(allData, 'report.attendee.without_event_user.not_confirmed'),
      total:
        _.sumBy(allData, 'report.attendee.with_event_user.total') +
        _.sumBy(allData, 'report.attendee.without_event_user.total'),
    },
    organizers: {
      confirmed: _.sumBy(allData, 'report.organizer.confirmed'),
      not_confirmed: _.sumBy(allData, 'report.organizer.not_confirmed'),
      total: _.sumBy(allData, 'report.organizer.total'),
    },
    collaborators: {
      confirmed: _.sumBy(allData, 'report.collaborator.confirmed'),
      not_confirmed: _.sumBy(allData, 'report.collaborator.not_confirmed'),
      total: _.sumBy(allData, 'report.collaborator.total'),
    },
    installers: {
      confirmed: _.sumBy(allData, 'report.installer.confirmed'),
      not_confirmed: _.sumBy(allData, 'report.installer.not_confirmed'),
      total: _.sumBy(allData, 'report.installer.total'),
    },
    activities: {
      confirmed: _.sumBy(allData, 'report.activity.confirmed'),
      not_confirmed: _.sumBy(allData, 'report.activity.not_confirmed'),
      total: _.sumBy(allData, 'report.activity.total'),
      details: parseActivitiesDetails(allData),
    },
    installations: {
      total: _.sumBy(allData, 'report.installation.total'),
      softwares: parseInstallationSoftwares(allData),
    },
  };
  return totals;
};

export const parseEvent = (event, eventsPrivateData = []) => {
  const {
    location,
    report: {attendee},
  } = event;
  const eventData = {
    locationDetail: {
      address_detail: location.slice(0, -3).join(' '),
      address: location[location.length - 3],
      province: location[location.length - 2],
    },
    assistanceDetail: {
      attendees: {
        confirmed:
          attendee.with_event_user.confirmed +
          attendee.without_event_user.confirmed,
        not_confirmed:
          attendee.with_event_user.not_confirmed +
          attendee.without_event_user.not_confirmed,
        total:
          attendee.with_event_user.total + attendee.without_event_user.total,
      },
    },
    ...event,
  };
  if (!_.isEmpty(eventsPrivateData)) {
    const privateData = _.find(eventsPrivateData, {id: event.id});
    if (!_.isEmpty(privateData)) return {...privateData, ...eventData};
  }
  return eventData;
};
