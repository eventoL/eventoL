import Cookies from 'js-cookie';

const getCsrf = () => Cookies.get('csrftoken');

export const addQueryString = (url, query) => {
  const queryKeys = query ? Object.keys(query) : [];
  if (queryKeys.length > 0) {
    const params = queryKeys.map(k => `${k}=${encodeURIComponent(query[k])}`);
    return `${url}?${params.join('&')}`;
  }
  return url;
};

const genericFetch = (url, queryString, params) => {
  const newUrl = addQueryString(url, queryString);
  return fetch(newUrl, params)
    .then(res => {
      if (!res.ok) {
        return Promise.reject(res.status, res.statusText);
      }
      return res.json();
    })
    .catch(status => {
      if (status === 403) {
        window.location.hash = '/';
        window.location.href = '/';
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

export const postUrl = (url, data, queryString) => {
  const newUrl = addQueryString(url, queryString);
  return fetch(newUrl, {
    method: 'POST',
    headers: {
      Accept: 'application/json, text/plain, */*',
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrf(),
    },
    body: JSON.stringify(data || {}),
    credentials: 'same-origin',
  }).then(res => res.json());
};
