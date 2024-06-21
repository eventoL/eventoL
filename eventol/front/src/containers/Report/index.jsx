import _ from 'lodash';
import React, {useState, useEffect, useRef, useCallback} from 'react';
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

const Report = props => {
  const exportButtonRef = useRef(null);

  const [table, setTable] = useState('confirmed');
  const [autoupdate, setAutoupdate] = useState(false);
  const [loading, setLoading] = useState(true);

  const [apiData, setApiData] = useState({
    data: [],
    count: 0,
    totals: {},
    pages: null,
  });
  const {communicator, eventsPrivateData} = props;

  const updateTable = useCallback(() => {
    if (autoupdate) window.location.reload();
  }, [autoupdate]);

  const loadToggleAutoupdate = useCallback(() => {
    let autoupdateState = localStorage.getItem('autoupdate');
    if (_.isNull(autoupdateState)) autoupdateState = false;
    else autoupdateState = JSON.parse(autoupdateState);
    if (autoupdate !== autoupdateState) {
      setAutoupdate(autoupdateState);
    }
  }, [autoupdate]);

  useEffect(() => {
    communicator.addOnMessage(updateTable);
    loadToggleAutoupdate();
  }, [communicator, loadToggleAutoupdate, updateTable]);

  const fetchData = ({pageSize, page, sorted, filtered}) => {
    loadReports(pageSize, page, sorted, filtered)
      .then(({count, results}) => {
        const quotient = Math.floor(count / pageSize);
        const remainder = count % pageSize;
        const pages = remainder > 0 ? quotient + 1 : quotient;
        const data = results.map(event => parseEvent(event, eventsPrivateData));
        const totals = parseTotals(results);

        setLoading(false);

        setApiData({
          data,
          count,
          pages,
          totals,
        });
      })
      .catch(err => Logger.error(gettext('There has been an error'), err));
  };

  const handleToggleAutoupdate = () => {
    localStorage.setItem('autoupdate', !autoupdate);
    setAutoupdate(!autoupdate);
  };

  const {data, count, totals, pages} = apiData;

  return (
    <div>
      <Title label={gettext('National report')}>
        <Toggle
          checked={autoupdate}
          effect="echo"
          label={gettext('Autoupdate')}
          labelPosition="left"
          name={gettext('Autoupdate')}
          onChange={handleToggleAutoupdate}
        />

        <Button
          handleOnClick={setTable}
          label={gettext('Assistance (confirmed)')}
          name="confirmed"
          type="success"
        />

        <Button
          handleOnClick={setTable}
          label={gettext('Assistance detail')}
          name="assitance"
          type="success"
        />

        <Button
          handleOnClick={setTable}
          label={gettext('Installations')}
          name="installations"
          type="success"
        />

        <Button
          handleOnClick={setTable}
          label={gettext('Activities')}
          name="activities"
          type="success"
        />

        <ExportButton
          ref={exportButtonRef}
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
        exportButton={exportButtonRef.current}
        fetchData={fetchData}
        isLoading={loading}
        pages={pages}
        table={table}
        totals={totals}
      />
    </div>
  );
};

Report.propTypes = {
  communicator: PropTypes.shape({
    addOnMessage: PropTypes.func.isRequired,
  }).isRequired,
  eventsPrivateData: PropTypes.arrayOf(PropTypes.shape()),
};

Report.defaultProps = {
  eventsPrivateData: [],
};

export default Report;
