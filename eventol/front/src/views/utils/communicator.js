import WsCommunicator from '../../utils/WsCommunicator';

/* eslint-disable-next-line import/prefer-default-export */
export const getCommunicator = properties => new WsCommunicator({
  /* eslint-disable-next-line camelcase */
  ws_url: `${properties.ws_protocol || 'ws'}://${window.location.host}/updates/`, // TODO: move to url utils
  reconnect: true,
});
