import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';

import ExportButton from '../ExportButton';
import {getColumns} from '../../utils/table';

import 'react-table/react-table.css';

const ReportTable = props => {
  const {
    data,
    pages,
    isLoading,
    defaultRows,
    fetchData,
    exportButton,
    table,
    eventsPrivateData,
    count,
    totals,
  } = props;
  const columns = getColumns(table, eventsPrivateData, count, totals);
  if (exportButton) exportButton.updateCsv(columns);
  return (
    <ReactTable
      className="-striped -highlight"
      columns={columns}
      data={data}
      defaultPageSize={defaultRows}
      defaultSorted={[{id: 'name', desc: false}]}
      loading={isLoading}
      manual
      multiSort={false}
      noDataText={gettext("There isn't any event yet.")}
      onFetchData={fetchData}
      pages={pages}
      pageSizeOptions={[5, 10, 15, 20, 25, 50, 100]}
      sortable={false}
    />
  );
};

ReportTable.propTypes = {
  count: PropTypes.number,
  data: PropTypes.arrayOf(PropTypes.shape()),
  defaultRows: PropTypes.number,
  eventsPrivateData: PropTypes.arrayOf(PropTypes.shape()),
  exportButton: PropTypes.instanceOf(ExportButton),
  fetchData: PropTypes.func.isRequired,
  isLoading: PropTypes.bool,
  pages: PropTypes.number,
  table: PropTypes.string,
  totals: PropTypes.shape(),
};

ReportTable.defaultProps = {
  count: 0,
  data: [],
  defaultRows: 0,
  eventsPrivateData: [],
  exportButton: null,
  isLoading: true,
  pages: 0,
  table: '',
  totals: {},
};

export default ReportTable;
