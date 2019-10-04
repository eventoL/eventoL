import _ from 'lodash';
import React from 'react';
import PropTypes from 'prop-types';
import Toggle from 'react-input-toggle';

import Logger from '../../utils/logger';
import Title from '../../components/Title';
import Button from '../../components/Button';
import ReportTable from '../../components/ReportTable';
import ExportButton from '../../components/ExportButton';

import {loadReports} from '../../utils/api';
import {parseTotals, parseEvent} from '../../utils/report';

import './react-input-toggle.css';
import 'react-table/react-table.css';

export default class Report extends React.PureComponent {
  static propTypes = {
    communicator: PropTypes.shape({
      addOnMessage: PropTypes.func.isRequired,
    }).isRequired,
    eventsPrivateData: PropTypes.arrayOf(PropTypes.shape()),
  };

  static defaultProps = {
    eventsPrivateData: [],
  };

  state = {
    table: 'confirmed',
    count: 0,
    autoupdate: false,
    data: [],
    totals: {},
    pages: null,
    loading: true,
  };

  componentDidMount() {
    const {communicator} = this.props;
    communicator.addOnMessage(this.updateTable);
    this.loadToggleAutoupdate();
  }

  fetchData = ({pageSize, page, sorted, filtered}) => {
    const {eventsPrivateData} = this.props;
    loadReports(pageSize, page, sorted, filtered)
      .then(({count, results}) => {
        const quotient = Math.floor(count / pageSize);
        const remainder = count % pageSize;
        const pages = remainder > 0 ? quotient + 1 : quotient;
        const data = results.map(event => parseEvent(event, eventsPrivateData));
        const totals = parseTotals(results);
        this.setState({
          count,
          data,
          loading: false,
          pages,
          totals,
        });
      })
      .catch(err => Logger.error(gettext('There has been an error'), err));
  };

  onClick = table => this.setState({table});

  loadToggleAutoupdate = () => {
    let autoupdate = localStorage.getItem('autoupdate');
    if (_.isNull(autoupdate)) autoupdate = false;
    else autoupdate = JSON.parse(autoupdate);
    this.setState({autoupdate});
  };

  handleToggleAutoupdate = () => {
    const {autoupdate} = this.state;
    localStorage.setItem('autoupdate', !autoupdate);
    this.setState({autoupdate: !autoupdate});
  };

  updateTable = () => {
    const {autoupdate} = this.state;
    if (autoupdate) window.location.reload();
  };

  render() {
    const {data, pages, loading, count, table, totals, autoupdate} = this.state;
    const {eventsPrivateData} = this.props;
    return (
      <div>
        <Title label={gettext('National report')}>
          <Toggle
            checked={autoupdate}
            effect="echo"
            label={gettext('Autoupdate')}
            labelPosition="left"
            name={gettext('Autoupdate')}
            onChange={this.handleToggleAutoupdate}
          />
          <Button
            handleOnClick={this.onClick}
            label={gettext('Assistance (confirmed)')}
            name="confirmed"
            type="success"
          />
          <Button
            handleOnClick={this.onClick}
            label={gettext('Assistance detail')}
            name="assitance"
            type="success"
          />
          <Button
            handleOnClick={this.onClick}
            label={gettext('Installations')}
            name="installations"
            type="success"
          />
          <Button
            handleOnClick={this.onClick}
            label={gettext('Activities')}
            name="activities"
            type="success"
          />
          <ExportButton
            ref={exportButton => {
              this.exportButton = exportButton;
            }}
            data={data}
            filename={table}
            label={gettext('Export')}
            type="success"
          />
        </Title>
        <ReportTable
          count={count}
          data={data}
          defaultRows={15}
          eventsPrivateData={eventsPrivateData}
          exportButton={this.exportButton}
          fetchData={this.fetchData}
          isLoading={loading}
          pages={pages}
          table={table}
          totals={totals}
        />
      </div>
    );
  }
}
