import React from 'react';
import PropTypes from 'prop-types';
import {CSVLink} from 'react-csv';

import './index.scss';

export default class ExportButton extends React.PureComponent {
  static propTypes = {
    data: PropTypes.arrayOf(
      PropTypes.oneOfType([PropTypes.string, PropTypes.number])
    ),
    filename: PropTypes.string,
    label: PropTypes.string,
    type: PropTypes.oneOf([
      'default',
      'primary',
      'success',
      'info',
      'warning',
      'danger',
      'link',
    ]),
  };

  static defaultProps = {
    data: [],
    filename: 'export',
    label: '',
    type: 'default',
  };

  state = {
    header: [],
    rows: [],
    totals: [],
  };

  getField = (columns, field) => {
    const values = [];
    columns.forEach(column => {
      if (!column.hasOwnProperty('Header')) return null;
      if (!column.hasOwnProperty('columns')) values.push(column[field]);
      else column.columns.forEach(subcolumn => values.push(subcolumn[field]));
      return column;
    });
    return values;
  };

  getRows(columns) {
    const {data} = this.props;
    const accessors = this.getField(columns, 'accessor');
    return data.map(row =>
      accessors.map(accessor => this.runAccessor(accessor, row))
    );
  }

  runAccessor = (accessor, row) => {
    if (typeof accessor === 'string') return row[accessor];
    return accessor(row);
  };

  updateCsv(columns) {
    const {data} = this.props;
    if (data.length > 0) {
      const header = this.getField(columns, 'Header');
      const rows = this.getRows(columns);
      const totals = this.getField(columns, 'total');
      this.setState({header, rows, totals});
    }
  }

  render() {
    const {type, label, filename} = this.props;
    const {header, rows, totals} = this.state;
    const csvData = [header, ...rows, totals];
    return (
      <div className={`export btn btn-raised btn-${type}`}>
        <CSVLink data={csvData} filename={`${filename}.csv`}>
          {label}
        </CSVLink>
      </div>
    );
  }
}
