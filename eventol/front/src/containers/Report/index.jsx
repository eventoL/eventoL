import _ from 'lodash';
import React from 'react';
import PropTypes from 'prop-types';
import Toggle from 'react-input-toggle';

import Title from '../../components/Title';
import Button from '../../components/Button';
import TableReport from '../../components/ReportTable';
import ExportButton from '../../components/ExportButton';

import {getUrl} from '../../utils/api';
import {REPORT_REQUIRED_FIELDS} from '../../utils/constants';

import './react-input-toggle.css';
import 'react-table/react-table.css';


export default class Report extends React.Component {
  static propTypes = {
    communicator: PropTypes.object,
    eventsPrivateData: PropTypes.object,
  }

  state = {
    all_data: [],
    columns: {},
    table: 'confirmed',
    count: 0,
    autoupdate: false,
    data: [],
    totals: {},
    pages: null,
    loading: true,
  }

  componentDidMount(){
    const {communicator} = this.props;
    communicator.addOnMessage(this.updateTable);
    let autoupdate = localStorage.getItem('autoupdate');
    if (autoupdate === null) autoupdate = false;
    else autoupdate = JSON.parse(autoupdate);
    this.setState({loading: true, autoupdate});
    const url = '/api/events/?limit=5000&offset=0&fields=report';
    return getUrl(url).then(
      ({results: all_data}) => this.setState({
        all_data, totals: this.parseTotals(all_data), loading: false,
      }),
    ).catch(err => console.error(gettext('There has been an error'), err));
  }

  loadContent(pageSize, page, sorted){
    const offset = page * pageSize;
    let queryParams = `limit=${pageSize}&offset=${offset}&fields=${REPORT_REQUIRED_FIELDS}`;
    if (sorted && sorted.length > 0){
      const [{id: name, desc}] = sorted;
      queryParams += `&ordering=${(desc) ? '-' : ''}${name}`;
    }
    const url = `/api/events/?${queryParams}`;
    return getUrl(url);
  }

  parseInstallationSoftwares = all_data => {
    const softwares = new Set();
    all_data.forEach(event => Object.keys(event.report.installation.software_count).forEach(key => softwares.add(key)));
    const installationsSoftwares = {};
    softwares.forEach(software => {
      const sum = _.sumBy(all_data, `report.installation.software_count.${software}`);
      installationsSoftwares[software] = sum;
    });
    return installationsSoftwares;
  }

  parseActivitiesDetails = all_data => {
    const status = new Set();
    const types = new Set();
    const levels = new Set();
    all_data.forEach(event => {
      Object.keys(event.report.activity.status_count).forEach(key => status.add(key));
      Object.keys(event.report.activity.type_count).forEach(key => types.add(key));
      Object.keys(event.report.activity.level_count).forEach(key => levels.add(key));
    });
    const activityDetail = {types: {}, status: {}, levels: {}};
    status.forEach(element => {
      const sum = _.sumBy(all_data, `report.activity.status_count.${element}`);
      activityDetail.status[element] = sum;
    });
    types.forEach(type => {
      const sum = _.sumBy(all_data, `report.activity.type_count.${type}`);
      activityDetail.types[type] = sum;
    });
    levels.forEach(level => {
      const sum = _.sumBy(all_data, `report.activity.level_count.${level}`);
      activityDetail.levels[level] = sum;
    });
    return activityDetail;
  }

  parseTotals = all_data => ({
    speakers: _.sumBy(all_data, 'report.speakers'),
    attendees: {
      confirmed: _.sumBy(all_data, 'report.attendee.with_event_user.confirmed') + _.sumBy(all_data, 'report.attendee.without_event_user.confirmed'),
      not_confirmed: _.sumBy(all_data, 'report.attendee.with_event_user.not_confirmed') + _.sumBy(all_data, 'report.attendee.without_event_user.not_confirmed'),
      total: _.sumBy(all_data, 'report.attendee.with_event_user.total') + _.sumBy(all_data, 'report.attendee.without_event_user.total'),
    },
    organizers: {
      confirmed: _.sumBy(all_data, 'report.organizer.confirmed'),
      not_confirmed: _.sumBy(all_data, 'report.organizer.not_confirmed'),
      total: _.sumBy(all_data, 'report.organizer.total'),
    },
    collaborators: {
      confirmed: _.sumBy(all_data, 'report.collaborator.confirmed'),
      not_confirmed: _.sumBy(all_data, 'report.collaborator.not_confirmed'),
      total: _.sumBy(all_data, 'report.collaborator.total'),
    },
    installers: {
      confirmed: _.sumBy(all_data, 'report.installer.confirmed'),
      not_confirmed: _.sumBy(all_data, 'report.installer.not_confirmed'),
      total: _.sumBy(all_data, 'report.installer.total'),
    },
    activities: {
      confirmed: _.sumBy(all_data, 'report.activity.confirmed'),
      not_confirmed: _.sumBy(all_data, 'report.activity.not_confirmed'),
      total: _.sumBy(all_data, 'report.activity.total'),
      details: this.parseActivitiesDetails(all_data),
    },
    installations: {
      total: _.sumBy(all_data, 'report.installation.total'),
      softwares: this.parseInstallationSoftwares(all_data),
    },
  })

  parseEvent = event => {
    const {eventsPrivateData} = this.props;
    const privateData = _.find(eventsPrivateData, {id: event.id});
    const {location, report: {attendee}} = event;
    event = {
      locationDetail: {
        address_detail: location.slice(0, -3).join(' '),
        address: location[location.length - 3],
        province: location[location.length - 2],
      },
      assistanceDetail: {
        attendees: {
          confirmed: attendee.with_event_user.confirmed + attendee.without_event_user.confirmed,
          not_confirmed: attendee.with_event_user.not_confirmed + attendee.without_event_user.not_confirmed,
          total: attendee.with_event_user.total + attendee.without_event_user.total,
        },
      },
      ...event,
    };
    if (privateData) return {...privateData, ...event};
    return event;
  }

  fetchData = ({
    pageSize, page, sorted, filtered,
  }) => {
    this.setState({loading: true});
    this.loadContent(pageSize, page, sorted, filtered).then(
      ({count, results}) => {
        // Now just get the rows of data to your React Table (and update anything else like total pages or loading)
        const quotient = Math.floor(count / pageSize);
        const remainder = count % pageSize;
        const pages = (remainder > 0) ? quotient + 1 : quotient;
        this.setState({
          data: results.map(this.parseEvent), loading: false, count, pages,
        });
      },
    ).catch(err => console.error(gettext('There has been an error'), err));
  }

  onClick = name => this.setState({table: name})

  handleToggleAutoupdate = () => {
    const {autoupdate} = this.state;
    localStorage.setItem('autoupdate', !autoupdate);
    this.setState({autoupdate: !autoupdate});
  }

  updateTable = () => {
    const {autoupdate} = this.state;
    if (autoupdate) location.reload();
  }

  render(){
    const {
      data, pages, loading, count, table, totals, autoupdate,
    } = this.state;
    const {eventsPrivateData} = this.props;
    return (
      <div>
        <Title label={gettext('National report')}>
          <Toggle
            checked={autoupdate}
            effect='echo'
            label={gettext('Autoupdate')}
            labelPosition='left'
            name={gettext('Autoupdate')}
            onChange={this.handleToggleAutoupdate}
          />
          <Button handleOnClick={this.onClick} label={gettext('Assistance (confirmed)')} name='confirmed' type='success' />
          <Button handleOnClick={this.onClick} label={gettext('Assistance detail')} name='assitance' type='success' />
          <Button handleOnClick={this.onClick} label={gettext('Installations')} name='installations' type='success' />
          <Button handleOnClick={this.onClick} label={gettext('Activities')} name='activities' type='success' />
          <ExportButton
            data={data}
            filename={table}
            label={gettext('Export')}
            ref={exportButton => this.exportButton = exportButton}
            type='success'
          />
        </Title>
        <TableReport
          count={count}
          data={data}
          defaultRows={15}
          eventsPrivateData={eventsPrivateData}
          exportButton={this.exportButton}
          fetchData={this.fetchData}
          loading={loading}
          pages={pages}
          table={table}
          totals={totals}
        />
      </div>
    );
  }
}
