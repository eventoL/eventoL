import WsCommunicator from '../../utils/WsCommunicator';

export function getCommunicator(properties){
  return new WsCommunicator({
    ws_url: `${properties.ws_protocol || 'ws'}://${window.location.host}/updates/`,
    reconnect: true
  });
}
