export function getUrl(url){
  return fetch(url).then(resp => resp.json())
}
