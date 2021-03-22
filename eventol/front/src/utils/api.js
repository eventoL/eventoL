import _ from 'lodash';
import Cookies from 'js-cookie';

import Logger from './logger';
import {getReportUrl} from './urls';

export const getCsrf = () => Cookies.get('csrftoken');

export const addQueryString = (url, query) => {
  const queryKeys = query ? Object.keys(query) : [];
  if (!_.isEmpty(queryKeys)) {
    const params = queryKeys.map(k => `${k}=${encodeURIComponent(query[k])}`);
    return `${url}?${params.join('&')}`;
  }
  return url;
};

export const genericFetch = (url, queryString, params) => {
  const newUrl = addQueryString(url, queryString);
  return fetch(newUrl, params)
    .then(res => {
      if (res.ok) {
        return res.json();
      }
      return Promise.reject(res);
    })
    .catch(res => {
      if (res.status === 403) {
        window.location.hash = '/';
        window.location.href = '/';
        Logger.warning('Redirect to /', res.status, res.statusText);
      } else {
        Logger.error('There has been an error', res.status, res.statusText);
      }
    });
};

export const getUrl = (url, queryString) =>
  genericFetch(url, queryString, {
    method: 'GET',
    credentials: 'same-origin',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrf(),
    },
  });

export const postUrl = (url, data, queryString) =>
  genericFetch(url, queryString, {
    method: 'POST',
    headers: {
      Accept: 'application/json, text/plain, */*',
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrf(),
    },
    body: JSON.stringify(data),
    credentials: 'same-origin',
  });

export const loadReports = (pageSize, page, sorted) =>
  getUrl(getReportUrl(pageSize, page, sorted));
