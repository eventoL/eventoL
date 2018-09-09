import Cookies from 'js-cookie';

const getCsrf = () => Cookies.get('csrftoken');

export const addQueryString = (url, query) => {
  const queryKeys = query ? Object.keys(query) : [];
  if (queryKeys.length > 0) {
    const params = queryKeys.map(k => `${k}=${encodeURIComponent(query[k])}`);
    url += `?${params.join('&')}`;
    return url;
  }
  return url;
}

const genericFetch = (url, queryString, params) => {
  url = addQueryString(url, queryString);
  return fetch(url, params)
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
}

export const getUrl = (url, queryString) => {
  return genericFetch(url, queryString, {
    method: 'GET',
    credentials: 'same-origin',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrf()
    }
  })
};

export const postUrl = (url, data, queryString) => {
  url = addQueryString(url, queryString);
  return fetch(
    url, {
      method: 'POST',
      headers: {
        Accept: 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrf()
      },
      body: JSON.stringify(data || {}),
      credentials: 'same-origin'
    })
    .then(res => res.json())
    .catch(err => console.error(err));
}
