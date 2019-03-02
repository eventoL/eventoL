import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';

import 'react-table/react-table.css';


export default class ReportTable extends React.Component {
  static propTypes = {
    count: PropTypes.number,
    data: PropTypes.array,
    defaultRows: PropTypes.number,
    eventsPrivateData: PropTypes.object,
    exportButton: PropTypes.object,
    fetchData: PropTypes.func,
    loading: PropTypes.bool,
    pages: PropTypes.number,
    table: PropTypes.string,
    totals: PropTypes.object,
  };

  getEventColumns(){
    const {count} = this.props;
    return {
      Header: gettext('Event'),
      columns: [{
        Header: gettext('Name'), accessor: 'name', resizable: false, sortable: true, total: `${gettext('Events')}: ${count}`,
        minWidth: 150, Footer: (<span><strong>{gettext('Events')}:  </strong>{count}</span>)
      }]
    };
  }

  getOrganizersColumns(){
    return {
      Header: gettext('Organizers'),
      columns: [
        {Header: gettext('Email'), accessor: 'email'},
        {Header: gettext('Organizers'), accessor: 'organizers'}
      ]};
  }

  getLocationColumns(){
    return {
      Header: gettext('Location'),
      columns: [{
        Header: gettext('Address detail'), id: 'address_detail',
        accessor: ({locationDetail: {address_detail}}) => address_detail
      },{
        Header: gettext('Address'), id: 'address',
        accessor: ({locationDetail: {address}}) => address
      }, {
        Header: gettext('Province'), id: 'province',
        accessor: ({locationDetail: {province}}) => province
      }]
    };
  }

  getAssitanceConfirmatedColumns(){
    const {totals} = this.props;
    if (!totals.hasOwnProperty('attendees')) return {};
    return {
      Header: gettext('Assistance (confirmed)'),
      columns: [{
        Header: gettext('Attendees'), id: 'attendees',
        accessor: ({assistanceDetail: {attendees}}) => attendees.confirmed, total: totals.attendees.confirmed,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.attendees.confirmed}</span>)
      },{
        Header: gettext('Organizers'), id: 'organizer',
        accessor: ({report: {organizer}}) => organizer.confirmed, total: totals.organizers.confirmed,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.organizers.confirmed}</span>)
      },{
        Header: gettext('Collaborators'), id: 'collaborator',
        accessor: ({report: {collaborator}}) => collaborator.confirmed, total: totals.collaborators.confirmed,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.collaborators.confirmed}</span>)
      },{
        Header: gettext('Installers'), id: 'installer',
        accessor: ({report: {installer}}) => installer.confirmed, total: totals.installers.confirmed,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.installers.confirmed}</span>)
      },{
        Header: gettext('Speakers'),id: 'speakers',
        accessor: ({report: {speakers}}) => speakers, total: totals.speakers,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.speakers}</span>)
      }]
    };
  }

  getActivitiesColumns(){
    const {totals} = this.props;
    if (!totals.hasOwnProperty('activities')) return {};
    return {
      Header: gettext('Activities'),
      columns: [{
        Header: gettext('Activities'), id: 'activities',
        accessor: ({report: {activity: {total}}}) => total, total: totals.activities.confirmed,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.activities.confirmed}</span>)
      },{
        Header: gettext('Installations'), id: 'installations',
        accessor: ({report: {installation: {total}}}) => total, total: totals.installations.total,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.installations.total}</span>)
      }]
    };
  }

  getConfirmationColumnsBy(category, total_category, field, title){
    const {totals} = this.props;
    if (!totals.hasOwnProperty(total_category)) return {};
    return {
      Header: title,
      columns: [{
        Header: gettext('Confirmed'), id: `${title.toLowerCase()}_confirmed`,
        accessor: data => data[field][category].confirmed, total: totals[total_category].confirmed,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals[total_category].confirmed}</span>)
      },{
        Header: gettext('Not Confirmed'), id: `${title.toLowerCase()}_not_confirmed`,
        accessor: data => data[field][category].not_confirmed, total: totals[total_category].not_confirmed,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals[total_category].not_confirmed}</span>)
      },{
        Header: gettext('Total'), id: `${title.toLowerCase()}_total`,
        accessor: data => data[field][category].total, total: totals[total_category].total,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals[total_category].total}</span>)
      }]
    };
  }

  getAssistancesFullColumns(){
    const {totals} = this.props;
    if (!totals.hasOwnProperty('attendees')) return {};
    return {
      attendees: this.getConfirmationColumnsBy('attendees', 'attendees', 'assistanceDetail', 'Attendees'),
      collaborators: this.getConfirmationColumnsBy('collaborator', 'collaborators', 'report', 'Collaborators'),
      installers: this.getConfirmationColumnsBy('installer', 'installers', 'report', 'Installers'),
      organizers: this.getConfirmationColumnsBy('organizer', 'organizers', 'report', 'Organizers'),
      speakers: {
        Header: gettext('Speakers'),id: 'speakers',
        accessor: ({report: {speakers}}) => speakers, total: totals.speakers,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.speakers}</span>)
      }
    };
  }

  getSoftwaresColumns(){
    const {totals} = this.props;
    if (!totals.hasOwnProperty('installations')) return [];
    return Object.keys(totals.installations.softwares).map(software => {
      return {
        Header: software, id: `installations_${software}`,
        accessor: ({report: {installation: {software_count}}}) => software_count[software] || 0, total: totals.installations.softwares[software] || 0,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.installations.softwares[software] || 0}</span>)
      };
    });
  }

  getInstallationsColumns(){
    const {totals} = this.props;
    if (!totals.hasOwnProperty('installations')) return {};
    const softwaresColumns = this.getSoftwaresColumns();
    return {
      Header: gettext('Installations'),
      columns: [{
        Header: gettext('Quantity'), id: 'installations_quantity',
        accessor: ({report: {installation: {total}}}) => total, total: totals.installations.total,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.installations.total}</span>)
      },
      ...softwaresColumns]
    };
  }

  getActivitiesFieldsColumns(category, plural_category, names){
    const {totals} = this.props;
    if (!totals.hasOwnProperty('activities')) return [];
    return Object.keys(totals.activities.details[plural_category]).map(element => {
      const Header = (element !== 'None') ? names[element - 1] : gettext('Don\'t configured');
      return {
        Header, id: `activity_${category}_${element}`,
        accessor: ({report: {activity}}) => activity[`${category}_count`][element] || 0, total: totals.activities.details[plural_category][element] || 0,
        Footer: (<span><strong>{gettext('Total')}: </strong>{totals.activities.details[plural_category][element] || 0}</span>)
      };
    });
  }

  getActivitiesFullColumns(){
    const confirmationColumn = this.getConfirmationColumnsBy('activity', 'activities', 'report', 'Attendees');
    if (!confirmationColumn.hasOwnProperty('columns')) return [];
    const statusColumns = this.getActivitiesFieldsColumns('status', 'status', [gettext('Proposal'), gettext('Accepted'), gettext('Rejected')]);
    const typeColumns = this.getActivitiesFieldsColumns('type', 'types', [gettext('Talk'), gettext('Workshop'), gettext('Lightning talk'), gettext('Other')]);
    const levelColumns = this.getActivitiesFieldsColumns('level', 'levels', [gettext('Beginner'), gettext('Medium'), gettext('Advanced')]);
    confirmationColumn.columns = [
      ...confirmationColumn.columns,
      ...statusColumns,
      ...typeColumns,
      ...levelColumns,
    ];
    return confirmationColumn;
  }

  getColumns(){
    const {table, eventsPrivateData} = this.props;
    const eventColumns = this.getEventColumns();
    const locationColumns = this.getLocationColumns();
    const assistanceConfirmatedColumns = this.getAssitanceConfirmatedColumns();
    const activitiesColumns = this.getActivitiesColumns();
    const assistancesFullColumns = this.getAssistancesFullColumns();
    const installationsColumns = this.getInstallationsColumns();
    const activitiesFullColumns = this.getActivitiesFullColumns();
    const columns = [eventColumns, locationColumns];
    if (eventsPrivateData){
      const organizersColumns = this.getOrganizersColumns();
      columns.push(organizersColumns);
    }
    if (table === 'confirmed'){
      columns.push(assistanceConfirmatedColumns);
      columns.push(activitiesColumns);
    }
    if (table === 'installations'){
      columns.push(assistancesFullColumns.installers);
      columns.push(installationsColumns);
    }
    if (table === 'assitance'){
      columns.push(assistancesFullColumns.attendees);
      columns.push(assistancesFullColumns.collaborators);
      columns.push(assistancesFullColumns.installers);
      columns.push(assistancesFullColumns.organizers);
      columns.push(assistancesFullColumns.speakers);
    }
    if (table === 'activities'){
      columns.push(assistancesFullColumns.speakers);
      columns.push(activitiesFullColumns);
    }
    return columns;
  }

  render(){
    const {
      data, pages, loading, defaultRows, fetchData, exportButton,
    } = this.props;
    const columns = this.getColumns();
    if (exportButton) exportButton.updateCsv(columns);
    return (
      <ReactTable
        className='-striped -highlight'
        columns={columns}
        data={data}
        defaultPageSize={defaultRows}
        defaultSorted={[{id: 'name', desc: false}]}
        loading={loading}
        manual
        multiSort={false}
        noDataText={gettext('There isn\'t any event yet.')}
        onFetchData={fetchData}
        pageSizeOptions={[5, 10, 15, 20, 25, 50, 100]}
        pages={pages}
        sortable={false}
      />
    );
  }
}
