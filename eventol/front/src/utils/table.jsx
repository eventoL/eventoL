import React from 'react';

export const getOrganizersColumns = () => ({
  Header: gettext('Organizers'),
  columns: [
    {Header: gettext('Email'), accessor: 'email'},
    {Header: gettext('Organizers'), accessor: 'organizers'},
  ],
});

export const getLocationColumns = () => ({
  Header: gettext('Location'),
  columns: [
    {
      Header: gettext('Address detail'),
      id: 'address_detail',
      accessor: ({locationDetail: {address_detail: addressDetail}}) =>
        addressDetail,
    },
    {
      Header: gettext('Address'),
      id: 'address',
      accessor: ({locationDetail: {address}}) => address,
    },
    {
      Header: gettext('Province'),
      id: 'province',
      accessor: ({locationDetail: {province}}) => province,
    },
  ],
});

export const getEventColumns = count => ({
  Header: gettext('Event'),
  columns: [
    {
      Header: gettext('Name'),
      accessor: 'name',
      resizable: false,
      sortable: true,
      total: `${gettext('Events')}: ${count}`,
      minWidth: 150,
      Footer: (
        <span>
          <strong>{`${gettext('Events')}: `}</strong>
          {count}
        </span>
      ),
    },
  ],
});

export const getAssitanceConfirmatedColumns = totals => {
  if (!totals.hasOwnProperty('attendees')) return {};
  return {
    Header: gettext('Assistance (confirmed)'),
    columns: [
      {
        Header: gettext('Attendees'),
        id: 'attendees',
        accessor: ({assistanceDetail: {attendees}}) => attendees.confirmed,
        total: totals.attendees.confirmed,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals.attendees.confirmed}
          </span>
        ),
      },
      {
        Header: gettext('Organizers'),
        id: 'organizer',
        accessor: ({report: {organizer}}) => organizer.confirmed,
        total: totals.organizers.confirmed,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals.organizers.confirmed}
          </span>
        ),
      },
      {
        Header: gettext('Collaborators'),
        id: 'collaborator',
        accessor: ({report: {collaborator}}) => collaborator.confirmed,
        total: totals.collaborators.confirmed,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals.collaborators.confirmed}
          </span>
        ),
      },
      {
        Header: gettext('Installers'),
        id: 'installer',
        accessor: ({report: {installer}}) => installer.confirmed,
        total: totals.installers.confirmed,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals.installers.confirmed}
          </span>
        ),
      },
      {
        Header: gettext('Speakers'),
        id: 'speakers',
        accessor: ({report: {speakers}}) => speakers,
        total: totals.speakers,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals.speakers}
          </span>
        ),
      },
    ],
  };
};

export const getActivitiesColumns = totals => {
  if (!totals.hasOwnProperty('activities')) return {};
  return {
    Header: gettext('Activities'),
    columns: [
      {
        Header: gettext('Activities'),
        id: 'activities',
        accessor: ({
          report: {
            activity: {total},
          },
        }) => total,
        total: totals.activities.confirmed,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals.activities.confirmed}
          </span>
        ),
      },
      {
        Header: gettext('Installations'),
        id: 'installations',
        accessor: ({
          report: {
            installation: {total},
          },
        }) => total,
        total: totals.installations.total,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals.installations.total}
          </span>
        ),
      },
    ],
  };
};

export const getConfirmationColumnsBy = (
  totals,
  category,
  totalCategory,
  field,
  title
) => {
  if (!totals.hasOwnProperty(totalCategory)) return {};
  return {
    Header: title,
    columns: [
      {
        Header: gettext('Confirmed'),
        id: `${title.toLowerCase()}_confirmed`,
        accessor: data => data[field][category].confirmed,
        total: totals[totalCategory].confirmed,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals[totalCategory].confirmed}
          </span>
        ),
      },
      {
        Header: gettext('Not Confirmed'),
        id: `${title.toLowerCase()}_not_confirmed`,
        accessor: data => data[field][category].not_confirmed,
        total: totals[totalCategory].not_confirmed,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals[totalCategory].not_confirmed}
          </span>
        ),
      },
      {
        Header: gettext('Total'),
        id: `${title.toLowerCase()}_total`,
        accessor: data => data[field][category].total,
        total: totals[totalCategory].total,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals[totalCategory].total}
          </span>
        ),
      },
    ],
  };
};

export const getAssistancesFullColumns = totals => {
  if (!totals.hasOwnProperty('attendees')) return {};
  return {
    attendees: getConfirmationColumnsBy(
      totals,
      'attendees',
      'attendees',
      'assistanceDetail',
      'Attendees'
    ),
    collaborators: getConfirmationColumnsBy(
      totals,
      'collaborator',
      'collaborators',
      'report',
      'Collaborators'
    ),
    installers: getConfirmationColumnsBy(
      totals,
      'installer',
      'installers',
      'report',
      'Installers'
    ),
    organizers: getConfirmationColumnsBy(
      totals,
      'organizer',
      'organizers',
      'report',
      'Organizers'
    ),
    speakers: {
      Header: gettext('Speakers'),
      id: 'speakers',
      accessor: ({report: {speakers}}) => speakers,
      total: totals.speakers,
      Footer: (
        <span>
          <strong>{`${gettext('Total')}: `}</strong>
          {totals.speakers}
        </span>
      ),
    },
  };
};

export const getSoftwaresColumns = totals => {
  if (!totals.hasOwnProperty('installations')) return [];
  return Object.keys(totals.installations.softwares).map(software => {
    return {
      Header: software,
      id: `installations_${software}`,
      accessor: ({
        report: {
          installation: {software_count: softwareCount},
        },
      }) => softwareCount[software] || 0,
      total: totals.installations.softwares[software] || 0,
      Footer: (
        <span>
          <strong>{`${gettext('Total')}: `}</strong>
          {totals.installations.softwares[software] || 0}
        </span>
      ),
    };
  });
};

export const getInstallationsColumns = totals => {
  if (!totals.hasOwnProperty('installations')) return {};
  const softwaresColumns = getSoftwaresColumns(totals);
  return {
    Header: gettext('Installations'),
    columns: [
      {
        Header: gettext('Quantity'),
        id: 'installations_quantity',
        accessor: ({
          report: {
            installation: {total},
          },
        }) => total,
        total: totals.installations.total,
        Footer: (
          <span>
            <strong>{`${gettext('Total')}: `}</strong>
            {totals.installations.total}
          </span>
        ),
      },
      ...softwaresColumns,
    ],
  };
};

export const getActivitiesFieldsColumns = (
  totals,
  category,
  pluralCategory,
  names
) => {
  if (!totals.hasOwnProperty('activities')) return [];
  return Object.keys(totals.activities.details[pluralCategory]).map(element => {
    const Header =
      element !== 'None' ? names[element - 1] : gettext("Don't configured");
    return {
      Header,
      id: `activity_${category}_${element}`,
      accessor: ({report: {activity}}) =>
        activity[`${category}_count`][element] || 0,
      total: totals.activities.details[pluralCategory][element] || 0,
      Footer: (
        <span>
          <strong>{`${gettext('Total')}: `}</strong>
          {totals.activities.details[pluralCategory][element] || 0}
        </span>
      ),
    };
  });
};

export const getActivitiesFullColumns = totals => {
  const confirmationColumn = getConfirmationColumnsBy(
    totals,
    'activity',
    'activities',
    'report',
    'Attendees'
  );
  if (!confirmationColumn.hasOwnProperty('columns')) return [];
  const statusColumns = getActivitiesFieldsColumns(totals, 'status', 'status', [
    gettext('Proposal'),
    gettext('Accepted'),
    gettext('Rejected'),
  ]);
  const typeColumns = getActivitiesFieldsColumns(totals, 'type', 'types', [
    gettext('Talk'),
    gettext('Workshop'),
    gettext('Lightning talk'),
    gettext('Other'),
  ]);
  const levelColumns = getActivitiesFieldsColumns(totals, 'level', 'levels', [
    gettext('Beginner'),
    gettext('Medium'),
    gettext('Advanced'),
  ]);
  confirmationColumn.columns = [
    ...confirmationColumn.columns,
    ...statusColumns,
    ...typeColumns,
    ...levelColumns,
  ];
  return confirmationColumn;
};

export const getColumns = (table, eventsPrivateData, count, totals) => {
  const eventColumns = getEventColumns(count);
  const locationColumns = getLocationColumns();
  const assistanceConfirmatedColumns = getAssitanceConfirmatedColumns(totals);
  const activitiesColumns = getActivitiesColumns(totals);
  const assistancesFullColumns = getAssistancesFullColumns(totals);
  const installationsColumns = getInstallationsColumns(totals);
  const activitiesFullColumns = getActivitiesFullColumns(totals);
  const columns = [eventColumns, locationColumns];
  if (eventsPrivateData) {
    const organizersColumns = getOrganizersColumns();
    columns.push(organizersColumns);
  }
  if (table === 'confirmed') {
    columns.push(assistanceConfirmatedColumns);
    columns.push(activitiesColumns);
  }
  if (table === 'installations') {
    columns.push(assistancesFullColumns.installers);
    columns.push(installationsColumns);
  }
  if (table === 'assitance') {
    columns.push(assistancesFullColumns.attendees);
    columns.push(assistancesFullColumns.collaborators);
    columns.push(assistancesFullColumns.installers);
    columns.push(assistancesFullColumns.organizers);
    columns.push(assistancesFullColumns.speakers);
  }
  if (table === 'activities') {
    columns.push(assistancesFullColumns.speakers);
    columns.push(activitiesFullColumns);
  }
  return columns;
};
