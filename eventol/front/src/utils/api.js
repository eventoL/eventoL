import Cookies from 'js-cookie';


export function getUrl(url){
  return fetch(url, {
    method: 'GET',
    credentials: 'same-origin',
    headers: {
        'X-CSRFToken': Cookies.get('csrftoken'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
     }
   }).then(resp => resp.json())
}
